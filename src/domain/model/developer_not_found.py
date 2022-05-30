from src.domain.model.handle import Handle


class DeveloperNotFound(Exception):
    def __init__(self, handle: Handle, absent_on: list[str]) -> None:
        self.handle = handle
        self.absent_on = absent_on

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DeveloperNotFound):
            return NotImplemented
        return (self.handle, self.absent_on) == (other.handle, other.absent_on)
