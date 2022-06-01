import datetime
import unittest
from copy import copy

import freezegun

from src.domain.events.events import (
    DevelopersAreConnected,
    DevelopersAreNotConnected,
    Event,
)
from src.domain.events.store import EventStore
from src.domain.events.stream import EventStream
from src.domain.events.stream_id import EventStreamId
from src.domain.model.connection import Connection
from src.domain.model.connection_id import ConnectionId
from src.domain.model.developer import Developer
from src.domain.model.handle import Handle
from src.persistence.event_sourced_connection_repository import (
    EventSourcedConnectionRepository,
)


class SpyEventStore(EventStore):
    def __init__(self) -> None:
        self._events: dict[EventStreamId, list[Event]] = {}

    def store(self, stream: EventStream) -> None:
        if not stream.id in self._events:
            self._events[stream.id] = []
        self._events[stream.id].extend(stream.events)

    def withdraw(self, stream_id: EventStreamId) -> EventStream:
        return EventStream(stream_id, copy(self._events[stream_id]))


class EventSourcedConnectionRepositoryTestCase(unittest.TestCase):
    def test_stores_object_changes_using_event_store(self) -> None:
        first_handle = Handle("dev1")
        second_handle = Handle("dev2")
        event_store: EventStore = SpyEventStore()
        repository = EventSourcedConnectionRepository(event_store)
        with freezegun.freeze_time("2022-05-30"):
            connection = Connection.register(
                Developer(
                    first_handle,
                    follows=[second_handle, Handle("dev5")],
                    organizations=["org1", "org2", "org3"],
                ),
                Developer(
                    second_handle,
                    follows=[Handle("dev3"), Handle("dev5")],
                    organizations=["org1", "org2", "org3"],
                ),
            )
        repository.save(connection)
        self.assertEqual(
            EventStream(
                EventStreamId("dev1-dev2"),
                events=[
                    DevelopersAreNotConnected(
                        handles=(first_handle, second_handle),
                        registered_at=datetime.datetime(2022, 5, 30),
                    ),
                ],
            ),
            event_store.withdraw(
                EventStreamId.from_handles(first_handle, second_handle)
            ),
        )

    def test_restores_connection_from_past_events(self) -> None:
        first_handle = Handle("dev1")
        second_handle = Handle("dev2")
        event_store: EventStore = SpyEventStore()
        repository = EventSourcedConnectionRepository(event_store)
        with freezegun.freeze_time("2022-05-30"):
            connection = Connection.register(
                Developer(
                    first_handle,
                    follows=[second_handle, Handle("dev5")],
                    organizations=["org1", "org2", "org3"],
                ),
                Developer(
                    second_handle,
                    follows=[Handle("dev3"), Handle("dev5")],
                    organizations=["org1", "org3"],
                ),
            )
            repository.save(connection)
            connection2 = connection.register(
                Developer(
                    first_handle,
                    follows=[second_handle, Handle("dev5")],
                    organizations=["org1", "org2", "org3"],
                ),
                Developer(
                    second_handle,
                    follows=[first_handle, Handle("dev3"), Handle("dev5")],
                    organizations=["org1", "org3"],
                ),
            )
            repository.save(connection2)
            connection3 = connection.register(
                Developer(
                    first_handle,
                    follows=[second_handle, Handle("dev5")],
                    organizations=["org1", "org2", "org3"],
                ),
                Developer(
                    second_handle,
                    follows=[first_handle, Handle("dev3"), Handle("dev5")],
                    organizations=["org1", "org2", "org3"],
                ),
            )
            repository.save(connection3)
        new_connection = repository.restore(
            ConnectionId.from_handles(first_handle, second_handle)
        )
        self.assertListEqual(
            [
                DevelopersAreNotConnected(
                    handles=(first_handle, second_handle),
                    registered_at=datetime.datetime(2022, 5, 30),
                ),
                DevelopersAreConnected(
                    handles=(first_handle, second_handle),
                    registered_at=datetime.datetime(2022, 5, 30),
                    organizations={"org1", "org3"},
                ),
                DevelopersAreConnected(
                    handles=(first_handle, second_handle),
                    registered_at=datetime.datetime(2022, 5, 30),
                    organizations={"org1", "org2", "org3"},
                ),
            ],
            new_connection.history(),
            ("REAL HISTORY\n", new_connection.history()),
        )
