from typing import Callable

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Route

from src.main.app import (
    create_connection_register_query_handler,
    create_connection_usecase,
)
from src.web.resource import Resource
from src.web.resources.connected import ConnectedResource
from src.web.resources.connected_registry import ConnectedRegistryResource


def resource_factory(resource: Resource) -> Callable[[Request], Response]:
    def view_adapter(request: Request) -> Response:
        return resource.on_get(request)

    return view_adapter


def create_app() -> Starlette:
    routes = [
        Route(
            "/connected/realtime/{first_developer_handle}/{second_developer_handle}",
            resource_factory(ConnectedResource(use_case=create_connection_usecase())),
        ),
        Route(
            "/connected/register/{first_developer_handle}/{second_developer_handle}",
            resource_factory(
                ConnectedRegistryResource(
                    query_handler=create_connection_register_query_handler()
                ),
            ),
        ),
    ]
    web_api = Starlette(routes=routes)
    return web_api
