import unittest

from src.persistence.events.csv_event_store import CsvEventStore


class CsvEventStoreTestCase(unittest.TestCase):

    def test_stores_events_to_a_file(self) -> None:
        _ = CsvEventStore()