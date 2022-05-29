from src.app.are_developers_connected_query import AreDevelopersConnectedQuery
from src.app.developers_relation import DevelopersRelation
from src.app.query_handler import QueryHandler


class ConnectedQueryHandler(
    QueryHandler[AreDevelopersConnectedQuery, DevelopersRelation]
):
    def handle(self, query: AreDevelopersConnectedQuery) -> DevelopersRelation:
        raise NotImplementedError()
