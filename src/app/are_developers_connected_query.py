from dataclasses import dataclass


@dataclass(frozen=True)
class AreDevelopersConnectedOperation:
    first_developer: str
    second_developer: str
