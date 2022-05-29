from abc import ABC, abstractmethod
from typing import Generic, TypeVar

Query = TypeVar("Query")
Result = TypeVar("Result")


class QueryHandler(ABC, Generic[Query, Result]):
    @abstractmethod
    def handle(self, query: Query) -> Result:
        pass
