import json

import falcon


class StubResource:
    def on_get(self, request: falcon.Request, response: falcon.Response, first_developer_handle: str, second_developer_handle: str) -> None:
        response.media = {"connected": True}


def create_app() -> falcon.API:
    web_api = falcon.API()
    web_api.add_route("/connected/realtime/{first_developer_handle}/{second_developer_handle}", StubResource())
    return web_api
