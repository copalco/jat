import unittest

from src.app.are_developers_connected_query import AreDevelopersConnectedQuery
from src.app.connected_query_handler import ConnectedQueryHandler
from src.app.developers_relation import DevelopersConnected, DevelopersNotConnected
from src.domain.model.developer import Developer
from src.domain.model.developers_repository import DevelopersRepository
from src.domain.model.handle import Handle


class FakeDevelopersRepository(DevelopersRepository):
    def __init__(self) -> None:
        self._developers: dict[Handle, Developer] = {}

    def add_developer(self, developer: Developer) -> None:
        self._developers[developer.handle] = developer

    def get(self, handle: Handle) -> Developer:
        return self._developers[handle]


class ConnectedQueryHandlerTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = FakeDevelopersRepository()  # type: ignore

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
        result = ConnectedQueryHandler(self.repository).handle(
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
        result = ConnectedQueryHandler(self.repository).handle(
            AreDevelopersConnectedQuery(first_developer="dev1", second_developer="dev2")
        )
        self.assertEqual(
            DevelopersConnected(organisations=["org1", "org2"]).connected(),
            result.connected(),
        )
