import unittest

from src.domain.events.store import EventStore
from src.domain.events.stream import EventStream
from src.domain.events.stream_id import EventStreamId
from src.persistence.event_sourced_connection_repository import \
    EventSourcedConnectionRepository


class SpyEventStore(EventStore):
    def store(self, stream: EventStream) -> None:
        pass

    def withdraw(self, stream_id: EventStreamId) -> EventStream:
        pass


class EventSourcedRedemptionRepository(unittest.TestCase):

    def test_stores_object_changes_using_event_store(self) -> None:
        event_store: EventStore = SpyEventStore()
        _ = EventSourcedConnectionRepository(event_store)