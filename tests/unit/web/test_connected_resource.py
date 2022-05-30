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
from src.app.errors import Errors
from src.domain.model.developer_not_found import DeveloperNotFound
from src.domain.model.handle import Handle
from src.web.resources.connected import ConnectedResource


class FakeQueryHandler(ConnectedQueryHandler):
    def __init__(self) -> None:
        self._connected = ["dev1", "dev2"]
        self._error: Exception | None = None

    def handle(self, query: AreDevelopersConnectedQuery) -> DevelopersRelation:
        if self._error:
            raise self._error
        if (
            query.first_developer in self._connected
            and query.second_developer in self._connected
        ):
            return DevelopersConnected(["org1", "org2"])
        return DevelopersNotConnected()

    def fail_with(self, error: Exception) -> None:
        self._error = error


class ConnectedResourceTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.query_handler = FakeQueryHandler()  # type: ignore
        self.resource = ConnectedResource(self.query_handler)

    def test_returns_false_for_not_connected_developers(self) -> None:
        result = self.resource.on_get(
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
        result = self.resource.on_get(
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
            JSONResponse({"connected": True, "organizations": ["org1", "org2"]}).body,
            result.body,
        )

    def test_returns_errors_list_on_errors(self) -> None:
        self.query_handler.fail_with(
            Errors(
                [DeveloperNotFound(Handle("dev1"), absent_on=["twitter", "github"]), DeveloperNotFound(Handle("dev2"), absent_on=["twitter"])]
            )
        )
        result = self.resource.on_get(
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
            JSONResponse({
                "errors": [
                    "dev1 is no valid user in github",
                    "dev1 is no valid user in twitter",
                    "dev2 is no valid user in twitter",
                ]
            }
            ).body,
            result.body,
        )
