import datetime
from dataclasses import dataclass

from src.domain.model.handle import Handle


@dataclass
class Event:
    registered_at: datetime.datetime

    def to_csv_row(self) -> list[str]:
        return [self.registered_at.isoformat()]

    @classmethod
    def from_csv_row(cls, row: list[str]) -> "Event":
        match row:
            case [str(), str(), str()]:
                return DevelopersAreConnected.from_csv_row(row)
            case [str(), str()]:
                return DevelopersAreNotConnected.from_csv_row(row)
            case _:
                raise NotImplementedError()


@dataclass
class DevelopersAreConnected(Event):
    handles: tuple[Handle, Handle]
    organizations: set[str]

    def to_csv_row(self) -> list[str]:
        result = super().to_csv_row()
        result.append(f"{self.handles[0]}-{self.handles[1]}")
        result.append(",".join(self.organizations))
        return result

    @classmethod
    def from_csv_row(cls, row: list[str]) -> "Event":
        registered_at = datetime.datetime.fromisoformat(row[0])
        first_raw_handle, second_raw_handle = row[1].split("-")
        handles = (Handle(first_raw_handle), Handle(second_raw_handle))
        organizations = set(org for org in row[2].split(",") if org != ",")
        return cls(
            registered_at=registered_at, handles=handles, organizations=organizations
        )


@dataclass
class DevelopersAreNotConnected(Event):
    handles: tuple[Handle, Handle]

    def to_csv_row(self) -> list[str]:
        result = super().to_csv_row()
        result.append(f"{self.handles[0]}-{self.handles[1]}")
        return result

    @classmethod
    def from_csv_row(cls, row: list[str]) -> "Event":
        registered_at = datetime.datetime.fromisoformat(row[0])
        first_raw_handle, second_raw_handle = row[1].split("-")
        handles = (Handle(first_raw_handle), Handle(second_raw_handle))
        return cls(registered_at=registered_at, handles=handles)
