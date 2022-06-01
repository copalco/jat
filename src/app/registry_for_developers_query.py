from dataclasses import dataclass


@dataclass(frozen=True)
class ConnectedRegistryForDevelopersQuery:
    first: str
    second: str
