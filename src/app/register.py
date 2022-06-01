from dataclasses import dataclass

from src.app.entry import Entry
from src.domain.model.handle import Handle


@dataclass(frozen=True)
class RegisterFor:
    first: Handle
    second: Handle
    entries: list[Entry]
