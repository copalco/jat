from abc import ABC, abstractmethod

from src.domain.model.developer import Developer
from src.domain.model.developer_not_found import DeveloperNotFound


class Result(ABC):
    @classmethod
    def ok(cls, value: Developer) -> "Result":
        return Correct(value)

    @classmethod
    def error(cls, value: DeveloperNotFound) -> "Result":
        return Error(value)

    @abstractmethod
    def succeeded(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def value(self) -> Developer:
        raise NotImplementedError()

    @abstractmethod
    def errors(self) -> list[DeveloperNotFound]:
        raise NotImplementedError()


class Correct(Result):
    def __init__(self, value: Developer) -> None:
        self._value = value

    def succeeded(self) -> bool:
        return True

    def value(self) -> Developer:
        return self._value

    def errors(self) -> list[DeveloperNotFound]:
        return []


class Error(Result):
    def __init__(self, value: DeveloperNotFound) -> None:
        self._value = value

    def succeeded(self) -> bool:
        return False

    def value(self) -> Developer:
        raise NotImplementedError()

    def errors(self) -> list[DeveloperNotFound]:
        return [self._value]
