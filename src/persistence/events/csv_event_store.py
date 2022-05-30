from src.domain.events.store import EventStore
from src.domain.events.stream import EventStream
from src.domain.events.stream_id import EventStreamId


class CsvEventStore(EventStore):
    def store(self, stream: EventStream) -> None:
        raise NotImplementedError()

    def withdraw(self, stream_id: EventStreamId) -> EventStream:
        raise NotImplementedError()
