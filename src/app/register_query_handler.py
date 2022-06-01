from src.app.register import RegisterFor
from src.app.registry_for_developers_query import ConnectedRegistryForDevelopersQuery
from src.domain.model.handle import Handle


class ConnectedRegistryQueryHandler:
    def handle(self, query: ConnectedRegistryForDevelopersQuery) -> RegisterFor:
        return RegisterFor(Handle(""), Handle(""), [])
