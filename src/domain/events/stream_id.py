from dataclasses import dataclass

from src.domain.model.handle import Handle


@dataclass(frozen=True)
class EventStreamId:
    _value: str

    @classmethod
    def from_handles(
        cls, first_handle: Handle, second_handle: Handle
    ) -> "EventStreamId":
        return cls(f"{first_handle}-{second_handle}")

    def to_raw_handles(self) -> tuple[str, str]:
        raw_handles = self._value.split("-")
        return (raw_handles[0], raw_handles[1])

    def __str__(self) -> str:
        return self._value
