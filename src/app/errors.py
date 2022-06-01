from src.domain.model.developer_not_found import DeveloperNotFound


class Errors(Exception):
    def __init__(self, errors: list[DeveloperNotFound]) -> None:
        self._errors = errors

    def list(self) -> list[DeveloperNotFound]:
        return self._errors
