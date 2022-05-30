import abc

from src.domain.events.stream import EventStream
from src.domain.events.stream_id import EventStreamId


class EventStore(abc.ABC):

    @abc.abstractmethod
    def store(self, stream: EventStream) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def withdraw(self, stream_id: EventStreamId) -> EventStream:
        raise NotImplementedError()
