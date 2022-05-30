from src.domain.model.handle import Handle


class DeveloperNotFound(Exception):
    def __init__(self, handle: Handle, absent_on: list[str]) -> None:
        self.handle = handle
        self.absent_on = absent_on
