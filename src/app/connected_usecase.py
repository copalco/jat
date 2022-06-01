from src.app.are_developers_connected_query import AreDevelopersConnectedOperation
from src.app.developers_relation import DevelopersRelation
from src.app.developers_result import Result
from src.app.errors import Errors
from src.app.query_handler import UseCase
from src.domain.model.connection import Connection
from src.domain.model.connection_repository import ConnectionRepository
from src.domain.model.developer import Developer
from src.domain.model.developer_not_found import DeveloperNotFound
from src.domain.model.developers_repository import DevelopersRepository
from src.domain.model.handle import Handle


class ConnectedUseCase(UseCase[AreDevelopersConnectedOperation, DevelopersRelation]):
    def __init__(
        self,
        developers_repository: DevelopersRepository,
        connection_repository: ConnectionRepository,
    ) -> None:
        self._connection_repository = connection_repository
        self._developer_repository = developers_repository

    def handle(self, operation: AreDevelopersConnectedOperation) -> DevelopersRelation:
        errors: list[Exception] = []
        first_developer: Developer | None = None
        second_developer: Developer | None = None
        try:
            first_developer = self._developer_repository.get(
                Handle(operation.first_developer)
            )
        except DeveloperNotFound as e:
            errors.append(e)
        try:
            second_developer = self._developer_repository.get(
                Handle(operation.second_developer)
            )
        except DeveloperNotFound as e:
            errors.append(e)
        if errors:
            raise Errors(errors)
        connection = Connection.register(first_developer, second_developer)
        self._connection_repository.save(connection)
        if connection.are_connected():
            return DevelopersConnected(organizations=connection.shared_organizations())
        return DevelopersNotConnected()
