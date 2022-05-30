from abc import ABC, abstractmethod

from src.domain.model.connection import Connection


class ConnectionRepository(ABC):
    @abstractmethod
    def save(self, connection: Connection) -> None:
        pass
