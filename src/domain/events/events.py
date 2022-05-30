import datetime
from dataclasses import dataclass

from src.domain.model.handle import Handle


@dataclass
class Event:
    registered_at: datetime.datetime


@dataclass
class DevelopersAreConnected(Event):
    handles: tuple[Handle, Handle]
    organizations: set[str]


@dataclass
class DevelopersAreNotConnected(Event):
    handles: tuple[Handle, Handle]
