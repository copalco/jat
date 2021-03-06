import abc
from dataclasses import dataclass

from src.domain.model.connection import Connection


class DevelopersRelation(abc.ABC):
    @abc.abstractmethod
    def connected(self) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    def organizations(self) -> list[str]:
        raise NotImplementedError()

    @classmethod
    def from_connection(cls, connection: Connection) -> "DevelopersRelation":
        if not connection.are_connected():
            return DevelopersNotConnected()
        return DevelopersConnected(connection.shared_organizations())


@dataclass(frozen=True)
class DevelopersConnected(DevelopersRelation):
    _organizations: list[str]

    def connected(self) -> bool:
        return True

    def organizations(self) -> list[str]:
        return self._organizations


@dataclass(frozen=True)
class DevelopersNotConnected(DevelopersRelation):
    def connected(self) -> bool:
        return False

    def organizations(self) -> list[str]:
        return []
