from dataclasses import dataclass


@dataclass
class TwitterUser:
    followed_by: list[str]
    following: list[str]
