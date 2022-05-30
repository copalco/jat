from dataclasses import dataclass


@dataclass
class TwitterUser:
    username: str
    follows: list[str]
