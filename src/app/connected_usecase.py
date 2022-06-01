from src.app.are_developers_connected_query import AreDevelopersConnectedOperation
from src.app.developers_relation import DevelopersRelation
from src.app.developers_result import Result
from src.app.errors import Errors
from src.app.query_handler import UseCase
from src.domain.model.connection import Connection
from src.domain.model.connection_id import ConnectionId
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
        first_developer, second_developer = self._developers(operation)
        connection = Connection(
            ConnectionId.from_handles(first_developer.handle, second_developer.handle)
        )
        connection.register(first_developer, second_developer)
        self._connection_repository.save(connection)
        return DevelopersRelation.from_connection(connection)

    def _developers(
        self, operation: AreDevelopersConnectedOperation
    ) -> tuple[Developer, Developer]:
        first = self._retrieve(operation.first_developer)
        second = self._retrieve(operation.second_developer)
        if not first.succeeded() or not second.succeeded():
            raise Errors(errors=first.errors() + second.errors())
        return first.value(), second.value()

    def _retrieve(self, handle: str) -> Result:
        try:
            return Result.ok(self._developer_repository.get(Handle(handle)))
        except DeveloperNotFound as e:
            return Result.error(e)
