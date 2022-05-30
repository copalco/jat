import datetime
import tempfile
import unittest

from src.domain.events.events import DevelopersAreConnected, DevelopersAreNotConnected
from src.domain.events.stream import EventStream
from src.domain.events.stream_id import EventStreamId
from src.domain.model.handle import Handle
from src.persistence.events.csv_event_store import CsvEventStore


class CsvEventStoreTestCase(unittest.TestCase):
    def test_stores_events_to_a_file(self) -> None:
        dir = tempfile.TemporaryDirectory(prefix="testing_csv")
        handles = (Handle("dev1"), Handle("dev2"))
        before = datetime.datetime(2022, 5, 30, 0)
        after = datetime.datetime(2022, 5, 30, 1)
        event_stream_id = EventStreamId.from_handles(*handles)
        event_stream = EventStream(
            event_stream_id,
            events=[
                DevelopersAreConnected(
                    registered_at=before,
                    handles=handles,
                    organizations={"org1", "org2"},
                ),
                DevelopersAreNotConnected(registered_at=after, handles=handles),
            ],
        )
        store = CsvEventStore(f"{dir.name}/events.csv")
        store.store(event_stream)
        _ = store.withdraw(event_stream_id)
