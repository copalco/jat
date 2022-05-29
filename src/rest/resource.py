import abc

from starlette.requests import Request
from starlette.responses import Response


class Resource(abc.ABC):
    @abc.abstractmethod
    def on_get(self, request: Request) -> Response:
        raise NotImplementedError
