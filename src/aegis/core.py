from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional
from uuid import uuid4


class ConflictError(RuntimeError):
    """Raised when a mutation targets a stale state revision."""


@dataclass(frozen=True)
class Event:
    id: str
    workflow_id: str
    type: str
    payload: Dict[str, Any]
    actor: str
    revision: int
    created_at: str


@dataclass(frozen=True)
class Checkpoint:
    id: str
    workflow_id: str
    revision: int
    state: Dict[str, Any]
    created_at: str


@dataclass
class StateStore:
    _states: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    _revisions: Dict[str, int] = field(default_factory=dict)
    _events: Dict[str, List[Event]] = field(default_factory=dict)
    _checkpoints: Dict[str, List[Checkpoint]] = field(default_factory=dict)
    _processed_keys: Dict[str, set[str]] = field(default_factory=dict)

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def load(self, workflow_id: str) -> tuple[Dict[str, Any], int]:
        return dict(self._states.get(workflow_id, {})), self._revisions.get(workflow_id, 0)

    def commit(
        self,
        workflow_id: str,
        base_revision: int,
        changes: Dict[str, Any],
        actor: str,
        event_type: str = "state.committed",
        event_payload: Optional[Dict[str, Any]] = None,
        idempotency_key: Optional[str] = None,
    ) -> int:
        if idempotency_key and idempotency_key in self._processed_keys.setdefault(workflow_id, set()):
            return self._revisions.get(workflow_id, 0)

        current_revision = self._revisions.get(workflow_id, 0)
        if base_revision != current_revision:
            raise ConflictError(
                f"stale revision for {workflow_id}: expected {current_revision}, got {base_revision}"
            )

        state = dict(self._states.get(workflow_id, {}))
        state.update(changes)
        next_revision = current_revision + 1
        self._states[workflow_id] = state
        self._revisions[workflow_id] = next_revision

        event = Event(
            id=str(uuid4()),
            workflow_id=workflow_id,
            type=event_type,
            payload=dict(event_payload or changes),
            actor=actor,
            revision=next_revision,
            created_at=self._now(),
        )
        self._events.setdefault(workflow_id, []).append(event)
        if idempotency_key:
            self._processed_keys.setdefault(workflow_id, set()).add(idempotency_key)
        return next_revision

    def checkpoint(self, workflow_id: str) -> Checkpoint:
        state, revision = self.load(workflow_id)
        checkpoint = Checkpoint(
            id=str(uuid4()),
            workflow_id=workflow_id,
            revision=revision,
            state=state,
            created_at=self._now(),
        )
        self._checkpoints.setdefault(workflow_id, []).append(checkpoint)
        return checkpoint

    def events(self, workflow_id: str) -> Iterable[Event]:
        return tuple(self._events.get(workflow_id, ()))

    def latest_checkpoint(self, workflow_id: str) -> Optional[Checkpoint]:
        checkpoints = self._checkpoints.get(workflow_id, [])
        return checkpoints[-1] if checkpoints else None


@dataclass
class Workflow:
    workflow_id: str
    store: StateStore

    def load_state(self) -> "WorkflowState":
        state, revision = self.store.load(self.workflow_id)
        return WorkflowState(self, state, revision)

    def checkpoint(self) -> Checkpoint:
        return self.store.checkpoint(self.workflow_id)

    def resume(self) -> "WorkflowState":
        checkpoint = self.store.latest_checkpoint(self.workflow_id)
        if checkpoint is None:
            return self.load_state()
        return WorkflowState(self, dict(checkpoint.state), checkpoint.revision)


@dataclass(frozen=True)
class WorkflowState:
    workflow: Workflow
    data: Dict[str, Any]
    revision: int

    def commit(
        self,
        changes: Dict[str, Any],
        actor: str = "unknown",
        event_type: str = "state.committed",
        event_payload: Optional[Dict[str, Any]] = None,
        idempotency_key: Optional[str] = None,
    ) -> "WorkflowState":
        revision = self.workflow.store.commit(
            workflow_id=self.workflow.workflow_id,
            base_revision=self.revision,
            changes=changes,
            actor=actor,
            event_type=event_type,
            event_payload=event_payload,
            idempotency_key=idempotency_key,
        )
        updated, _ = self.workflow.store.load(self.workflow.workflow_id)
        return WorkflowState(self.workflow, updated, revision)
