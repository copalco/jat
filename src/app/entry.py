import datetime
from dataclasses import dataclass


@dataclass(frozen=True)
class Entry:
    registered_at: datetime.datetime
    connected: bool
    organizations: list[str]
