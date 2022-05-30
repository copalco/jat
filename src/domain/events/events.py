import datetime
from dataclasses import dataclass


@dataclass
class Event:
    registered_at: datetime.datetime


@dataclass
class DevelopersAreConnected(Event):
    organizations: set[str]


@dataclass
class DevelopersAreNotConnected(Event):
    pass
