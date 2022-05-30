from src.domain.events.store import EventStore
from src.domain.events.stream import EventStream
from src.domain.events.stream_id import EventStreamId
from src.domain.model.connection import Connection


class EventSourcedConnectionRepository:
    def __init__(self, event_store: EventStore) -> None:
        self._event_store = event_store

    def save(self, connection: Connection) -> None:
        stream = EventStream(
            EventStreamId.from_handles(*connection.handles),
            events=connection.changes(),
        )
        self._event_store.store(stream)
