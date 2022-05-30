import unittest

from src.app.are_developers_connected_query import AreDevelopersConnectedQuery
from src.app.connected_query_handler import ConnectedQueryHandler
from src.app.developers_relation import DevelopersConnected, DevelopersNotConnected
from src.app.errors import Errors
from src.domain.model.connection import Connection
from src.domain.model.connection_repository import ConnectionRepository
from src.domain.model.developer import Developer
from src.domain.model.developer_not_found import DeveloperNotFound
from src.domain.model.developers_repository import DevelopersRepository
from src.domain.model.handle import Handle


class FakeDevelopersRepository(DevelopersRepository):
    def __init__(self) -> None:
        self._developers: dict[Handle, Developer] = {}
        self._errors: list[Exception] = []

    def add_developer(self, developer: Developer) -> None:
        self._developers[developer.handle] = developer

    def get(self, handle: Handle) -> Developer:
        if self._errors:
            raise self._errors.pop()
        return self._developers[handle]

    def raise_errors(self, errors: list[Exception]) -> None:
        self._errors = errors
        self._errors.reverse()


class SpyConnectionRepository(ConnectionRepository):
    def __init__(self) -> None:
        self._connections: dict[tuple[Handle, Handle], Connection] = {}

    def save(self, connection: Connection) -> None:
        self._connections[connection.handles] = connection

    def stored_connection_for(self, first: Handle, second: Handle) -> Connection:
        return self._connections[(first, second)]


class ConnectedQueryHandlerTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = FakeDevelopersRepository()  # type: ignore
        self.connection_repository = SpyConnectionRepository()  # type: ignore
        self.query_handler = ConnectedQueryHandler(self.repository, self.connection_repository)  # type: ignore

    def test_developers_not_being_connected(self) -> None:
        self.repository.add_developer(
            Developer(
                Handle("dev1"),
                follows=[Handle("dev3")],
                followed_by=[Handle("dev2")],
                organizations=["a", "b", "c"],
            )
        )
        self.repository.add_developer(
            Developer(
                Handle("dev2"),
                follows=[Handle("dev1")],
                followed_by=[Handle("dev3")],
                organizations=["a", "b", "c"],
            )
        )
        result = self.query_handler.handle(
            AreDevelopersConnectedQuery(first_developer="dev1", second_developer="dev2")
        )
        self.assertEqual(DevelopersNotConnected().connected(), result.connected())

    def test_developers_are_connected(self) -> None:
        self.repository.add_developer(
            Developer(
                Handle("dev1"),
                follows=[Handle("dev2")],
                followed_by=[Handle("dev2")],
                organizations=["a", "b", "c"],
            )
        )
        self.repository.add_developer(
            Developer(
                Handle("dev2"),
                follows=[Handle("dev1")],
                followed_by=[Handle("dev1")],
                organizations=["a", "b", "c"],
            )
        )
        result = self.query_handler.handle(
            AreDevelopersConnectedQuery(first_developer="dev1", second_developer="dev2")
        )
        self.assertEqual(
            DevelopersConnected(organizations={"a", "b", "c"}).connected(),
            result.connected(),
        )

    def test_on_developer_erros_collects_them_and_raises_as_one(self) -> None:
        self.repository.raise_errors(
            errors=[
                DeveloperNotFound(Handle("dev1"), absent_on=["twitter", "github"]),
                DeveloperNotFound(Handle("dev2"), absent_on=["github"]),
            ]
        )
        self.repository.add_developer(
            Developer(
                Handle("dev1"),
                follows=[Handle("dev2")],
                followed_by=[Handle("dev2")],
                organizations=["a", "b", "c"],
            )
        )
        self.repository.add_developer(
            Developer(
                Handle("dev2"),
                follows=[Handle("dev1")],
                followed_by=[Handle("dev1")],
                organizations=["a", "b", "c"],
            )
        )
        with self.assertRaises(Errors) as exception_info:
            _ = self.query_handler.handle(
                AreDevelopersConnectedQuery(
                    first_developer="dev1", second_developer="dev2"
                )
            )
        self.assertEqual(
            str(exception_info.exception),
            str(
                Errors(
                    [
                        DeveloperNotFound(
                            Handle("dev1"), absent_on=["twitter", "github"]
                        ),
                        DeveloperNotFound(Handle("dev2"), absent_on=["github"]),
                    ]
                )
            ),
        )

    def test_stores_registered_connection(self) -> None:
        self.repository.add_developer(
            Developer(
                Handle("dev1"),
                follows=[Handle("dev2")],
                followed_by=[Handle("dev2")],
                organizations=["a", "b", "c"],
            )
        )
        self.repository.add_developer(
            Developer(
                Handle("dev2"),
                follows=[Handle("dev1")],
                followed_by=[Handle("dev1")],
                organizations=["a", "b", "c"],
            )
        )
        result = self.query_handler.handle(
            AreDevelopersConnectedQuery(first_developer="dev1", second_developer="dev2")
        )
        self.assertTrue(
            self.connection_repository.stored_connection_for(
                Handle("dev1"), Handle("dev2")
            )
        )
        self.assertEqual(
            DevelopersConnected(organizations={"a", "b", "c"}).connected(),
            result.connected(),
        )
