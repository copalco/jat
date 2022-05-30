from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from src.app.are_developers_connected_query import AreDevelopersConnectedQuery
from src.app.connected_query_handler import ConnectedQueryHandler
from src.app.errors import Errors
from src.web.resource import Resource


class StubResource(Resource):
    def on_get(self, request: Request) -> Response:
        return JSONResponse({"connected": True, "organizations": []})


class ConnectedResource(Resource):
    def __init__(self, query_handler: ConnectedQueryHandler) -> None:
        self.query_handler = query_handler

    def on_get(self, request: Request) -> Response:
        try:
            relation = self.query_handler.handle(
                AreDevelopersConnectedQuery(
                    request.path_params["first_developer_handle"],
                    request.path_params["second_developer_handle"],
                )
            )
        except Errors as e:
            errors = []
            for error in e.args[0]:
                for service in error.absent_on:
                    errors.append(f"{error.handle} is no valid user in {service}")
            return JSONResponse({"errors": sorted(errors)})
        else:
            if relation.connected():
                return JSONResponse(
                    {"connected": True, "organizations": relation.organizations()}
                )
            return JSONResponse({"connected": False})
