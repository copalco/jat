from dataclasses import dataclass

from src.domain.model.handle import Handle


@dataclass
class ConnectionId:
    _first: Handle
    _second: Handle

    @classmethod
    def from_handles(cls, first: Handle, second: Handle) -> "ConnectionId":
        return cls(first, second)

    @classmethod
    def from_raw(cls, handles: tuple[str, str]) -> "ConnectionId":
        return cls(Handle(handles[0]), Handle(handles[1]))

    def to_handles(self) -> tuple[Handle, Handle]:
        return (self._first, self._second)

    def __str__(self) -> str:
        return f"{self._first}-{self._second}"
