from abc import ABC
from abc import abstractmethod

from src.app.are_developers_connected_query import AreDevelopersConnectedQuery
from src.app.developers_relation import DevelopersRelation


class ConnectedQueryHandler(ABC):

    @abstractmethod
    def query(self, query: AreDevelopersConnectedQuery) -> DevelopersRelation:
        pass
