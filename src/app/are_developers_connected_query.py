from dataclasses import dataclass


@dataclass(frozen=True)
class AreDevelopersConnectedQuery:
    first_developer: str
    second_developer: str
