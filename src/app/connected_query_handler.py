from src.app.are_developers_connected_query import AreDevelopersConnectedQuery
from src.app.developers_relation import DevelopersRelation
from src.app.errors import Errors
from src.app.query_handler import QueryHandler
from src.domain.model.connection import Connection
from src.domain.model.connection_repository import ConnectionRepository
from src.domain.model.developer import Developer
from src.domain.model.developer_not_found import DeveloperNotFound
from src.domain.model.developers_repository import DevelopersRepository
from src.domain.model.handle import Handle


class ConnectedQueryHandler(
    QueryHandler[AreDevelopersConnectedQuery, DevelopersRelation]
):
    def __init__(
        self,
        developers_repository: DevelopersRepository,
        connection_repository: ConnectionRepository,
    ) -> None:
        self._connection_repository = connection_repository
        self._developer_repository = developers_repository

    def handle(self, query: AreDevelopersConnectedQuery) -> DevelopersRelation:
        errors: list[Exception] = []
        first_developer: Developer | None = None
        second_developer: Developer | None = None
        try:
            first_developer = self._developer_repository.get(
                Handle(query.first_developer)
            )
        except DeveloperNotFound as e:
            errors.append(e)
        try:
            second_developer = self._developer_repository.get(
                Handle(query.second_developer)
            )
        except DeveloperNotFound as e:
            errors.append(e)
        if errors:
            raise Errors(errors)
        if not first_developer or not second_developer:
            raise RuntimeError("Impossible!")
        connection = Connection.register(first_developer, second_developer)
        self._connection_repository.save(connection)
        return DevelopersRelation.from_connection(connection)
