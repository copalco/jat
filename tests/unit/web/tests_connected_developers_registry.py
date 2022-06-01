import datetime
import unittest

from starlette.requests import Request
from starlette.responses import JSONResponse

from src.app.entry import Entry
from src.app.register import RegisterFor
from src.app.register_query_handler import ConnectedRegistryQueryHandler
from src.app.registry_for_developers_query import ConnectedRegistryForDevelopersQuery
from src.web.resources.connected_registry import ConnectedRegistryResource


class FakeQueryHandler(ConnectedRegistryQueryHandler):
    def __init__(self) -> None:
        pass

    def handle(self, query: ConnectedRegistryForDevelopersQuery) -> RegisterFor:
        if query.first != "dev1" or query.second != "dev2":
            return RegisterFor(query.first, query.second, entries=[])
        return RegisterFor(
            "dev1",
            "dev2",
            entries=[
                Entry(
                    registered_at=datetime.datetime(2022, 5, 30),
                    connected=False,
                    organizations=[],
                ),
                Entry(
                    registered_at=datetime.datetime(2022, 6, 1),
                    connected=True,
                    organizations=["org1", "org3"],
                ),
                Entry(
                    registered_at=datetime.datetime(2022, 6, 2),
                    connected=True,
                    organizations=["org1", "org2", "org3"],
                ),
            ],
        )


class ConnectedResourceTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.query_handler = FakeQueryHandler()  # type: ignore
        self.resource = ConnectedRegistryResource(self.query_handler)  # type: ignore

    def test_returns_registered_entries_for_developers(self) -> None:
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
            JSONResponse(
                [
                    {
                        "registered_at": datetime.datetime(2022, 5, 30).isoformat(),
                        "connected": False,
                    },
                    {
                        "registered_at": datetime.datetime(2022, 6, 1).isoformat(),
                        "connected": True,
                        "organisations": ["org1", "org3"],
                    },
                    {
                        "registered_at": datetime.datetime(2022, 6, 2).isoformat(),
                        "connected": True,
                        "organisations": ["org1", "org2", "org3"],
                    },
                ]
            ).body,
            result.body,
            result.body,
        )

    def test_returns_empty_list_for_developers_never_checked_for_connection(
        self,
    ) -> None:
        result = self.resource.on_get(
            Request(
                scope={
                    "type": "http",
                    "path_params": {
                        "first_developer_handle": "dev99999",
                        "second_developer_handle": "dev22222",
                    },
                }
            )
        )
        self.assertEqual(JSONResponse([]).body, result.body, result.body)
