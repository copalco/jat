from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from src.app.entry import Entry
from src.app.register_query_handler import ConnectedRegistryQueryHandler
from src.app.registry_for_developers_query import ConnectedRegistryForDevelopersQuery
from src.web.resource import Resource


class ConnectedRegistryResource(Resource):
    def __init__(self, query_handler: ConnectedRegistryQueryHandler) -> None:
        self._query_handler = query_handler

    def on_get(self, request: Request) -> Response:
        register = self._query_handler.handle(
            ConnectedRegistryForDevelopersQuery(
                request.path_params["first_developer_handle"],
                request.path_params["second_developer_handle"],
            )
        )
        return JSONResponse(
            [self._serialize_entry(entry) for entry in register.entries]
        )

    def _serialize_entry(self, entry: Entry) -> dict[str, str | bool | list[str]]:
        serialized: dict[str, str | bool | list[str]] = {
            "registered_at": entry.registered_at.isoformat(),
            "connected": entry.connected,
        }
        if entry.connected:
            serialized["organisations"] = entry.organizations
        return serialized
