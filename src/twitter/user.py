from dataclasses import dataclass


@dataclass
class TwitterUser:
    username: str
    followed_by: list[str]
    follows: list[str]
