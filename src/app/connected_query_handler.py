from src.app.are_developers_connected_query import AreDevelopersConnectedQuery
from src.app.developers_relation import DevelopersNotConnected, DevelopersRelation
from src.app.query_handler import QueryHandler
from src.domain.model.developers_repository import DevelopersRepository


class ConnectedQueryHandler(
    QueryHandler[AreDevelopersConnectedQuery, DevelopersRelation]
):
    def __init__(self, developers_repository: DevelopersRepository) -> None:
        self._repository = developers_repository

    def handle(self, query: AreDevelopersConnectedQuery) -> DevelopersRelation:
        return DevelopersNotConnected()
