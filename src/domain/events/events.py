import datetime
from dataclasses import dataclass

from src.domain.model.handle import Handle


@dataclass
class Event:
    registered_at: datetime.datetime

    def to_string(self) -> list[str]:
        return [self.registered_at.isoformat()]

    @classmethod
    def from_string(cls, event_string: list[str]) -> "Event":
        return cls(datetime.datetime.fromisoformat(event_string[0]))


@dataclass
class DevelopersAreConnected(Event):
    handles: tuple[Handle, Handle]
    organizations: set[str]

    def to_string(self) -> list[str]:
        result = super().to_string()
        result.append(str(self.handles))
        result.append(",".join(self.organizations))
        return result

    @classmethod
    def from_string(cls, event_string: list[str]) -> "Event":
        registered_at = super().from_string(event_string).registered_at
        first_raw_handle, _, second_raw_handle = event_string[1].split("-")
        handles = (Handle(first_raw_handle), Handle(second_raw_handle))
        organizations = set(org for org in event_string[2].split(",") if org != ",")
        return cls(
            registered_at=registered_at, handles=handles, organizations=organizations
        )


@dataclass
class DevelopersAreNotConnected(Event):
    handles: tuple[Handle, Handle]

    def to_string(self) -> list[str]:
        result = super().to_string()
        result.append(str(self.handles))
        return result

    @classmethod
    def from_string(cls, event_string: list[str]) -> "Event":
        registered_at = super().from_string(event_string).registered_at
        first_raw_handle, _, second_raw_handle = event_string[1].split("-")
        handles = (Handle(first_raw_handle), Handle(second_raw_handle))
        return cls(registered_at=registered_at, handles=handles)
