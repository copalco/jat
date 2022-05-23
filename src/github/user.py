from dataclasses import dataclass


@dataclass(frozen=True)
class GithubUser:
    username: str
    organizations: list[str]
