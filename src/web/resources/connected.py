from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from src.web.resource import Resource


class StubResource(Resource):
    def on_get(self, request: Request) -> Response:
        return JSONResponse({"connected": True, "organizations": []})
