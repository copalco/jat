import datetime
import unittest

import freezegun

from src.app.entry import Entry
from src.app.register import RegisterFor
from src.app.register_query_handler import ConnectedRegistryQueryHandler
from src.app.registry_for_developers_query import ConnectedRegistryForDevelopersQuery
from src.domain.model.connection import Connection
from src.domain.model.connection_id import ConnectionId
from src.domain.model.connection_repository import ConnectionRepository
from src.domain.model.developer import Developer
from src.domain.model.handle import Handle


class SpyConnectionRepository(ConnectionRepository):
    def __init__(self) -> None:
        self._connections: dict[tuple[Handle, Handle], Connection] = {}

    def save(self, connection: Connection) -> None:
        self._connections[connection.handles] = connection

    def restore(self, id: ConnectionId) -> Connection:
        try:
            return self._connections[id.to_handles()]
        except KeyError:
            return Connection.restore(id, [])


class ConnectedRegistryQueryHandlerTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.connection_repository = SpyConnectionRepository()  # type: ignore
        self.query_handler = ConnectedRegistryQueryHandler(  # type: ignore
            self.connection_repository
        )

    def test_returns_registry_for_developers(self) -> None:
        first_handle = Handle("dev1")
        second_handle = Handle("dev2")
        connection = Connection(ConnectionId.from_handles(first_handle, second_handle))
        with freezegun.freeze_time("2022-06-01"):
            connection.register(
                Developer(
                    first_handle,
                    follows=[Handle("dev3")],
                    organizations=["a", "b", "c"],
                ),
                Developer(
                    second_handle,
                    follows=[first_handle],
                    organizations=["a", "b", "c"],
                ),
            )
            connection.register(
                Developer(
                    first_handle,
                    follows=[second_handle],
                    organizations=["a", "b", "c"],
                ),
                Developer(
                    second_handle,
                    follows=[first_handle],
                    organizations=["a", "b", "c"],
                ),
            )
        self.connection_repository.save(connection)
        register = self.query_handler.handle(
            ConnectedRegistryForDevelopersQuery(first="dev1", second="dev2")
        )
        self.assertEqual(
            RegisterFor(
                "dev1",
                "dev2",
                entries=[
                    Entry(
                        registered_at=datetime.datetime(2022, 6, 1),
                        connected=False,
                        organizations=[],
                    ),
                    Entry(
                        registered_at=datetime.datetime(2022, 6, 1),
                        connected=True,
                        organizations=["a", "b", "c"],
                    ),
                ],
            ),
            register,
            register,
        )

    def test_returns_empty_register_for_never_checked_developers(self) -> None:
        register = self.query_handler.handle(
            ConnectedRegistryForDevelopersQuery(first="dev55", second="dev678")
        )
        self.assertEqual(RegisterFor("dev55", "dev678", entries=[]), register)
