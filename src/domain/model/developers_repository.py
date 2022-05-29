import abc

from src.domain.model.developer import Developer
from src.domain.model.handle import Handle


class DevelopersRepository(abc.ABC):
    @abc.abstractmethod
    def get(self, handle: Handle) -> Developer:
        pass
