import unittest

from starlette.requests import Request
from starlette.responses import JSONResponse

from src.web.resources.connected import ConnectedResource


class ConnectedResourceTestCase(unittest.TestCase):
    def test_returns_false_for_not_connected_developers(self) -> None:
        resource = ConnectedResource()
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
