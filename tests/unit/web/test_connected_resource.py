import unittest

from starlette.requests import Request
from starlette.responses import JSONResponse

from src.app.are_developers_connected_query import AreDevelopersConnectedQuery
from src.app.connected_query_handler import ConnectedQueryHandler
from src.app.developers_relation import (
    DevelopersConnected,
    DevelopersNotConnected,
    DevelopersRelation,
)
from src.web.resources.connected import ConnectedResource


class FakeQueryHandler(ConnectedQueryHandler):
    def __init__(self) -> None:
        self._connected = ["dev1", "dev2"]

    def handle(self, query: AreDevelopersConnectedQuery) -> DevelopersRelation:
        if (
            query.first_developer in self._connected
            and query.second_developer in self._connected
        ):
            return DevelopersConnected(["org1", "org2"])
        return DevelopersNotConnected()


class ConnectedResourceTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.query_handler = FakeQueryHandler()  # type: ignore

    def test_returns_false_for_not_connected_developers(self) -> None:
        resource = ConnectedResource(self.query_handler)
        result = resource.on_get(
            Request(
                scope={
                    "type": "http",
                    "path_params": {
                        "first_developer_handle": "dev1",
                        "second_developer_handle": "dev22",
                    },
                }
            )
        )
        self.assertEqual(JSONResponse({"connected": False}).body, result.body)

    def test_returns_true_for_connected_developers(self) -> None:
        resource = ConnectedResource(self.query_handler)
        result = resource.on_get(
            Request(
                scope={
                    "type": "http",
                    "path_params": {
                        "first_developer_handle": "dev1",
                        "second_developer_handle": "dev2",
                    },
                }
            )
        )
        self.assertEqual(
            JSONResponse({"connected": True, "organisations": ["org1", "org2"]}).body,
            result.body,
        )
