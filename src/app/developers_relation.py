import abc


class DevelopersRelation(abc.ABC):
    @abc.abstractmethod
    def connected(self) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    def organisations(self) -> list[str]:
        raise NotImplementedError()


class DevelopersConnected(DevelopersRelation):
    def __init__(self, organisations: list[str]) -> None:
        self._organisations = organisations

    def connected(self) -> bool:
        return True

    def organisations(self) -> list[str]:
        return self._organisations


class DevelopersNotConnected(DevelopersRelation):
    def connected(self) -> bool:
        return False

    def organisations(self) -> list[str]:
        raise NotImplementedError()
