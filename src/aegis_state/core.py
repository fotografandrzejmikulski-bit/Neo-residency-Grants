"""Minimal deterministic Aegis state primitives for the MVP."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


class ConflictError(RuntimeError):
    """Raised when a transaction is based on a stale state revision."""


class TransactionClosedError(RuntimeError):
    """Raised when a transaction is used after commit/rollback."""


@dataclass(frozen=True)
class Event:
    sequence: int
    event_type: str
    payload: dict[str, Any]
    worker_id: str


@dataclass(frozen=True)
class Checkpoint:
    revision: int
    data: dict[str, Any]


@dataclass
class WorkflowState:
    workflow_id: str
    revision: int = 0
    data: dict[str, Any] = field(default_factory=dict)
    events: list[Event] = field(default_factory=list)


class Transaction:
    def __init__(self, store: "InMemoryStore", workflow_id: str, base_revision: int):
        self._store = store
        self.workflow_id = workflow_id
        self.base_revision = base_revision
        self._changes: dict[str, Any] = {}
        self._events: list[tuple[str, dict[str, Any], str]] = []
        self._closed = False

    def _ensure_open(self) -> None:
        if self._closed:
            raise TransactionClosedError("transaction already closed")

    def set(self, key: str, value: Any) -> None:
        self._ensure_open()
        if not key:
            raise ValueError("state key must not be empty")
        self._changes[key] = value

    def append_event(
        self,
        event_type: str,
        payload: dict[str, Any],
        worker_id: str = "unknown",
    ) -> None:
        self._ensure_open()
        if not event_type:
            raise ValueError("event_type must not be empty")
        self._events.append((event_type, dict(payload), worker_id))

    def commit(self) -> WorkflowState:
        self._ensure_open()
        try:
            return self._store.commit(
                self.workflow_id,
                self.base_revision,
                self._changes,
                self._events,
            )
        finally:
            self._closed = True


class InMemoryStore:
    """Executable local reference model for Aegis semantics.

    This is not a production persistence layer. It exists to make correctness
    properties testable before a durable backend is introduced.
    """

    def __init__(self) -> None:
        self._states: dict[str, WorkflowState] = {}
        self._checkpoints: dict[str, dict[int, Checkpoint]] = {}

    def create(self, workflow_id: str) -> WorkflowState:
        if not workflow_id:
            raise ValueError("workflow_id must not be empty")
        if workflow_id in self._states:
            raise ValueError(f"workflow already exists: {workflow_id}")
        self._states[workflow_id] = WorkflowState(workflow_id=workflow_id)
        self._checkpoints[workflow_id] = {
            0: Checkpoint(revision=0, data={})
        }
        return self.snapshot(workflow_id)

    def snapshot(self, workflow_id: str) -> WorkflowState:
        state = self._states[workflow_id]
        return WorkflowState(
            workflow_id=state.workflow_id,
            revision=state.revision,
            data=dict(state.data),
            events=list(state.events),
        )

    def begin(self, workflow_id: str, base_revision: int | None = None) -> Transaction:
        state = self._states[workflow_id]
        revision = state.revision if base_revision is None else base_revision
        if revision < 0:
            raise ValueError("base_revision must be non-negative")
        return Transaction(self, workflow_id, revision)

    def commit(
        self,
        workflow_id: str,
        base_revision: int,
        changes: dict[str, Any],
        events: list[tuple[str, dict[str, Any], str]],
    ) -> WorkflowState:
        state = self._states[workflow_id]
        if state.revision != base_revision:
            raise ConflictError(
                f"stale revision: expected {base_revision}, current {state.revision}"
            )

        next_revision = state.revision + 1
        state.data.update(changes)
        next_sequence = len(state.events) + 1
        for offset, (event_type, payload, worker_id) in enumerate(events):
            state.events.append(
                Event(
                    sequence=next_sequence + offset,
                    event_type=event_type,
                    payload=dict(payload),
                    worker_id=worker_id,
                )
            )
        state.revision = next_revision
        return self.snapshot(workflow_id)

    def checkpoint(self, workflow_id: str) -> int:
        state = self._states[workflow_id]
        self._checkpoints[workflow_id][state.revision] = Checkpoint(
            revision=state.revision,
            data=dict(state.data),
        )
        return state.revision

    def latest_checkpoint(self, workflow_id: str) -> Checkpoint:
        checkpoints = self._checkpoints[workflow_id]
        return checkpoints[max(checkpoints)]

    def resume(self, workflow_id: str, revision: int | None = None) -> WorkflowState:
        state = self._states[workflow_id]
        checkpoints = self._checkpoints[workflow_id]
        target = state.revision if revision is None else revision
        eligible = [rev for rev in checkpoints if rev <= target]
        if not eligible:
            raise KeyError(f"no checkpoint at or before revision: {target}")
        checkpoint_revision = max(eligible)
        checkpoint = checkpoints[checkpoint_revision]

        replayed = dict(checkpoint.data)
        for event in state.events:
            if checkpoint_revision < event.sequence <= target:
                if event.event_type == "state.set":
                    key = event.payload["key"]
                    replayed[key] = event.payload["value"]

        return WorkflowState(
            workflow_id=workflow_id,
            revision=target,
            data=replayed,
            events=list(state.events),
        )
