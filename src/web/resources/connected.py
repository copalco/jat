from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from src.app.are_developers_connected_query import AreDevelopersConnectedQuery
from src.app.connected_query_handler import ConnectedQueryHandler
from src.web.resource import Resource


class StubResource(Resource):
    def on_get(self, request: Request) -> Response:
        return JSONResponse({"connected": True, "organizations": []})


class ConnectedResource(Resource):
    def __init__(self, query_handler: ConnectedQueryHandler) -> None:
        self.query_handler = query_handler

    def on_get(self, request: Request) -> Response:
        relation = self.query_handler.handle(AreDevelopersConnectedQuery())
        if relation.connected():
            return JSONResponse(
                {"connected": True, "organisations": relation.organisations()}
            )
        return JSONResponse({"connected": False})
