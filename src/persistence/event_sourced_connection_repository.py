from src.domain.events.store import EventStore
from src.domain.events.stream import EventStream
from src.domain.events.stream_id import EventStreamId
from src.domain.model.connection import Connection
from src.domain.model.connection_id import ConnectionId
from src.domain.model.connection_repository import ConnectionRepository


class EventSourcedConnectionRepository(ConnectionRepository):
    def __init__(self, event_store: EventStore) -> None:
        self._event_store = event_store

    def save(self, connection: Connection) -> None:
        stream = EventStream(
            EventStreamId.from_handles(*connection.handles),
            events=connection.changes(),
        )
        self._event_store.store(stream)

    def restore(self, id: ConnectionId) -> Connection:
        stream = self._event_store.withdraw(stream_id=EventStreamId(str(id)))
        connection_id = ConnectionId.from_raw(stream.id.to_raw_handles())
        return Connection.restore(connection_id, stream.events)
