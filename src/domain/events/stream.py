from dataclasses import dataclass

from src.domain.events.events import Event
from src.domain.events.stream_id import EventStreamId


@dataclass(frozen=True)
class EventStream:
    id: EventStreamId
    events: list[Event]
