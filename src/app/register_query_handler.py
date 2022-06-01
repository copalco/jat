from src.app.entry import Entry
from src.app.register import RegisterFor
from src.app.registry_for_developers_query import ConnectedRegistryForDevelopersQuery
from src.domain.model.connection_id import ConnectionId
from src.domain.model.connection_repository import ConnectionRepository


class ConnectedRegistryQueryHandler:
    def __init__(self, connection_repository: ConnectionRepository) -> None:
        self.connection_repository = connection_repository

    def handle(self, query: ConnectedRegistryForDevelopersQuery) -> RegisterFor:
        connection = self.connection_repository.restore(
            ConnectionId.from_raw((query.first, query.second))
        )
        return RegisterFor(
            query.first,
            query.second,
            entries=[Entry.out_of(event) for event in connection.history()],
        )
