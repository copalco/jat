from abc import ABC, abstractmethod

from src.domain.model.connection import Connection
from src.domain.model.connection_id import ConnectionId


class ConnectionRepository(ABC):
    @abstractmethod
    def save(self, connection: Connection) -> None:
        raise NotImplementedError()

    @abstractmethod
    def restore(self, id: ConnectionId) -> Connection:
        raise NotImplementedError()
