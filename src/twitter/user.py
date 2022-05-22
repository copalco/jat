from dataclasses import dataclass


@dataclass
class TwitterUser:
    username: str
    followed_by: list[str]
    following: list[str]
