import unittest

from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from src.web.resource import Resource


class ConnectedResource(Resource):
    def on_get(self, request: Request) -> Response:
        return JSONResponse({})


class ConnectedResourceTestCase(unittest.TestCase):
    def test_returns_false_for_not_connected_developers(self) -> None:
        resource = ConnectedResource()
        result = resource.on_get(Request(scope={"type": "http"}))
        self.assertEqual(JSONResponse({}).body, result.body)
