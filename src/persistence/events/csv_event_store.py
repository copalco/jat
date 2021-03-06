import csv

from src.domain.events.events import Event
from src.domain.events.store import EventStore
from src.domain.events.stream import EventStream
from src.domain.events.stream_id import EventStreamId


class CSVEventStore(EventStore):
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath

    def store(self, stream: EventStream) -> None:
        with open(self.filepath, "a") as events_file:
            writer = csv.writer(events_file, delimiter=";")
            for event in stream.events:
                writer.writerow([stream.id, *event.to_csv_row()])

    def withdraw(self, stream_id: EventStreamId) -> EventStream:
        events: list[Event] = []
        with open(self.filepath) as events_file:
            reader = csv.reader(events_file, delimiter=";")
            for row in reader:
                if EventStreamId(row[0]) == stream_id:
                    events.append(Event.from_csv_row(row[1:]))
        return EventStream(stream_id, events)
