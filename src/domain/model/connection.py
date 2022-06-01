import datetime

from src.domain.events.events import (
    DevelopersAreConnected,
    DevelopersAreNotConnected,
    Event,
)
from src.domain.model.connection_id import ConnectionId
from src.domain.model.developer import Developer
from src.domain.model.handle import Handle


class Connection:
    def __init__(self, id: ConnectionId) -> None:
        self._id = id
        self._connected: bool | None = None
        self._organizations: set[str] = set()
        self._history: list[Event] = []
        self._changes: list[Event] = []

    def register(self, first: Developer, second: Developer) -> None:
        if first.connected(second):
            self.connected(first.shared_organizations(second))
        else:
            self.not_connected()

    def are_connected(self) -> bool:
        if self._connected is None:
            raise ValueError("Unknown connection")
        return self._connected

    def shared_organizations(self) -> list[str]:
        return sorted(list(self._organizations))

    def connected(self, shared_organizations: set[str]) -> None:
        event = DevelopersAreConnected(
            handles=self.handles,
            registered_at=datetime.datetime.utcnow(),
            organizations=shared_organizations,
        )
        self._apply(event)
        self._changes.append(event)

    def _apply(self, event: Event) -> None:
        self._history.append(event)
        if isinstance(event, DevelopersAreNotConnected):
            self._connected = False
        if isinstance(event, DevelopersAreConnected):
            self._connected = True
            self._organizations = event.organizations

    def not_connected(self) -> None:
        event = DevelopersAreNotConnected(
            handles=self.handles,
            registered_at=datetime.datetime.utcnow(),
        )
        self._apply(event)
        self._changes.append(event)

    def changes(self) -> list[Event]:
        return self._changes

    def history(self) -> list[Event]:
        return self._history

    @property
    def handles(self) -> tuple[Handle, Handle]:
        return self._id.to_handles()

    @classmethod
    def restore(cls, id: ConnectionId, events: list[Event]) -> "Connection":
        connection = cls(id)
        for event in events:
            connection._apply(event)
        return connection
