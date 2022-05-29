from src.app.are_developers_connected_query import AreDevelopersConnectedQuery
from src.app.developers_relation import (
    DevelopersConnected,
    DevelopersNotConnected,
    DevelopersRelation,
)
from src.app.query_handler import QueryHandler
from src.domain.model.developers_repository import DevelopersRepository
from src.domain.model.handle import Handle


class ConnectedQueryHandler(
    QueryHandler[AreDevelopersConnectedQuery, DevelopersRelation]
):
    def __init__(self, developers_repository: DevelopersRepository) -> None:
        self._developer_repository = developers_repository

    def handle(self, query: AreDevelopersConnectedQuery) -> DevelopersRelation:
        first_developer_handle = Handle(query.first_developer)
        second_developer_handle = Handle(query.second_developer)
        first_developer = self._developer_repository.get(first_developer_handle)
        second_developer = self._developer_repository.get(second_developer_handle)
        if first_developer.connected(second_developer):
            return DevelopersConnected(organisations=[])
        return DevelopersNotConnected()
