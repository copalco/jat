import datetime

from src.domain.events.events import (
    DevelopersAreConnected,
    DevelopersAreNotConnected,
    Event,
)
from src.domain.model.developer import Developer
from src.domain.model.handle import Handle


class Connection:
    def __init__(self, first: Developer, second: Developer) -> None:
        self._first = first
        self._second = second
        self._changes: list[Event] = []
        self._connection: bool | None = None
        self._organizations: set[str] | None = None

    @classmethod
    def register(
        cls, first_developer: Developer, second_developer: Developer
    ) -> "Connection":
        connection = Connection(first_developer, second_developer)
        if connection.are_connected():
            connection._connected()
        else:
            connection._not_connected()
        return connection

    def are_connected(self) -> bool:
        return (
            self._follow_each_other()
            and self._share_at_least_one_organization_on_github()
        )

    def _follow_each_other(self) -> bool:
        return self._first.is_following_on_twitter(
            self._second
        ) and self._second.is_following_on_twitter(self._first)

    def _share_at_least_one_organization_on_github(self) -> bool:
        return bool(self._shared_organizations())

    def _shared_organizations(self) -> set[str]:
        return set(self._first.organizations).intersection(self._second.organizations)

    def _connected(self) -> None:
        event = DevelopersAreConnected(
            handles=self.handles,
            registered_at=datetime.datetime.utcnow(),
            organizations=self._shared_organizations(),
        )
        self._apply(event)
        self._changes.append(event)

    def _apply(self, event: Event) -> None:
        if isinstance(event, DevelopersAreNotConnected):
            self._connection = False
        if isinstance(event, DevelopersAreConnected):
            self._connection = True
            self._organizations = event.organizations

    def _not_connected(self):
        event = DevelopersAreNotConnected(
            handles=self.handles,
            registered_at=datetime.datetime.utcnow(),
        )
        self._apply(event)
        self._changes.append(event)

    def changes(self) -> list[Event]:
        return self._changes

    @property
    def handles(self) -> tuple[Handle, Handle]:
        return (self._first.handle, self._second.handle)
