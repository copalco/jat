from typing import Iterator

from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from src.app.are_developers_connected_query import AreDevelopersConnectedOperation
from src.app.connected_usecase import ConnectedUseCase
from src.app.errors import Errors
from src.web.resource import Resource


class StubResource(Resource):
    def on_get(self, request: Request) -> Response:
        return JSONResponse({"connected": True, "organizations": []})


class ConnectedResource(Resource):
    def __init__(self, use_case: ConnectedUseCase) -> None:
        self.use_case = use_case

    def on_get(self, request: Request) -> Response:
        try:
            relation = self.use_case.handle(
                AreDevelopersConnectedOperation(
                    request.path_params["first_developer_handle"],
                    request.path_params["second_developer_handle"],
                )
            )
        except Errors as e:
            return JSONResponse({"errors": sorted(self._error_messages_from(e))})
        else:
            if relation.connected():
                return JSONResponse(
                    {"connected": True, "organizations": relation.organizations()}
                )
            return JSONResponse({"connected": False})

    def _error_messages_from(self, errors: Errors) -> Iterator[str]:
        for error in errors.list():
            for service in error.absent_on:
                yield f"{error.handle} is no valid user in {service}"
