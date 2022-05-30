from dataclasses import dataclass

from src.domain.model.handle import Handle


@dataclass(frozen=True)
class EventStreamId:
    value: str

    @classmethod
    def from_handles(
        cls, first_handle: Handle, second_handle: Handle
    ) -> "EventStreamId":
        return cls(f"{first_handle}-{second_handle}")

    def __str__(self) -> str:
        return self.value
