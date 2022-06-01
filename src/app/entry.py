import datetime
from dataclasses import dataclass

from src.domain.events.events import (
    DevelopersAreConnected,
    DevelopersAreNotConnected,
    Event,
)


@dataclass(frozen=True)
class Entry:
    registered_at: datetime.datetime
    connected: bool
    organizations: list[str]

    @classmethod
    def out_of(cls, event: Event) -> "Entry":
        match event:
            case DevelopersAreNotConnected(registered_at, _):
                return cls(registered_at, False, [])
            case DevelopersAreConnected(registered_at, _, organizations):
                return cls(registered_at, True, sorted(organizations))
            case _:
                raise NotImplementedError()
