from abc import ABC, abstractmethod
from typing import Generic, TypeVar

Operation = TypeVar("Operation")
Result = TypeVar("Result")


class UseCase(ABC, Generic[Operation, Result]):
    @abstractmethod
    def handle(self, operation: Operation) -> Result:
        pass
