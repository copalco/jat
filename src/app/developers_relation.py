import abc


class DevelopersRelation(abc.ABC):
    @abc.abstractmethod
    def connected(self) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    def organizations(self) -> set[str]:
        raise NotImplementedError()


class DevelopersConnected(DevelopersRelation):
    def __init__(self, organizations: set[str]) -> None:
        self._organizations = organizations

    def connected(self) -> bool:
        return True

    def organizations(self) -> set[str]:
        return self._organizations


class DevelopersNotConnected(DevelopersRelation):
    def connected(self) -> bool:
        return False

    def organizations(self) -> set[str]:
        raise NotImplementedError()
