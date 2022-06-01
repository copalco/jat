from dataclasses import dataclass

from src.app.entry import Entry


@dataclass(frozen=True)
class RegisterFor:
    first: str
    second: str
    entries: list[Entry]
