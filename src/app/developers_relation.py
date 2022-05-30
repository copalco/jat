import abc


class DevelopersRelation(abc.ABC):
    @abc.abstractmethod
    def connected(self) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    def organizations(self) -> list[str]:
        raise NotImplementedError()


class DevelopersConnected(DevelopersRelation):
    def __init__(self, organizations: list[str]) -> None:
        self._organizations = organizations

    def connected(self) -> bool:
        return True

    def organizations(self) -> list[str]:
        return self._organizations

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DevelopersConnected):
            return NotImplemented
        if self.connected() != other.connected():
            return False
        else:
            return self.organizations() == other.organizations()


class DevelopersNotConnected(DevelopersRelation):
    def connected(self) -> bool:
        return False

    def organizations(self) -> list[str]:
        raise NotImplementedError()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DevelopersConnected):
            return NotImplemented
        return self.connected() == other.connected()
