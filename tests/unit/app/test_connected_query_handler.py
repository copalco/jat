import unittest

from src.app.are_developers_connected_query import AreDevelopersConnectedQuery
from src.app.connected_query_handler import ConnectedQueryHandler
from src.app.developers_relation import DevelopersNotConnected


class ConnectedQueryHandlerTestCase(unittest.TestCase):
    def test_always_results_with_developers_not_being_connected(self) -> None:
        result = ConnectedQueryHandler().handle(AreDevelopersConnectedQuery())
        self.assertEqual(DevelopersNotConnected().connected(), result.connected())
