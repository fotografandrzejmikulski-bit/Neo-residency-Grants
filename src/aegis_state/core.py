"""Minimal deterministic Aegis state primitives for the MVP."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


class ConflictError(RuntimeError):
    """Raised when a transaction is based on a stale state revision."""


@dataclass(frozen=True)
class Event:
    sequence: int
    event_type: str
    payload: dict[str, Any]
    worker_id: str


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

    def set(self, key: str, value: Any) -> None:
        if self._closed:
            raise RuntimeError("transaction already closed")
        self._changes[key] = value

    def append_event(self, event_type: str, payload: dict[str, Any], worker_id: str = "unknown") -> None:
        if self._closed:
            raise RuntimeError("transaction already closed")
        self._events.append((event_type, dict(payload), worker_id))

    def commit(self) -> WorkflowState:
        if self._closed:
            raise RuntimeError("transaction already closed")
        self._closed = True
        return self._store.commit(
            self.workflow_id,
            self.base_revision,
            self._changes,
            self._events,
        )


class InMemoryStore:
    """Reference implementation used to validate Aegis semantics locally.

    This is intentionally not a production persistence layer. Its purpose is
    to make the correctness contract executable before a durable backend is
    introduced.
    """

    def __init__(self) -> None:
        self._states: dict[str, WorkflowState] = {}
        self._checkpoints: dict[str, dict[int, dict[str, Any]]] = {}

    def create(self, workflow_id: str) -> WorkflowState:
        if workflow_id in self._states:
            raise ValueError(f"workflow already exists: {workflow_id}")
        self._states[workflow_id] = WorkflowState(workflow_id=workflow_id)
        self._checkpoints[workflow_id] = {0: {}}
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

        state.data.update(changes)
        for event_type, payload, worker_id in events:
            state.events.append(
                Event(
                    sequence=len(state.events) + 1,
                    event_type=event_type,
                    payload=dict(payload),
                    worker_id=worker_id,
                )
            )
        state.revision += 1
        return self.snapshot(workflow_id)

    def checkpoint(self, workflow_id: str) -> int:
        state = self._states[workflow_id]
        self._checkpoints[workflow_id][state.revision] = dict(state.data)
        return state.revision

    def resume(self, workflow_id: str, revision: int | None = None) -> WorkflowState:
        state = self._states[workflow_id]
        target = state.revision if revision is None else revision
        checkpoints = self._checkpoints[workflow_id]
        if target not in checkpoints:
            raise KeyError(f"checkpoint not found: {target}")
        return WorkflowState(
            workflow_id=workflow_id,
            revision=target,
            data=dict(checkpoints[target]),
        )
