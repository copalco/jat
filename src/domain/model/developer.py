from dataclasses import dataclass

from src.domain.model.handle import Handle


@dataclass
class Developer:
    handle: Handle
    organizations: list[str]

    def connected(self, developer: "Developer") -> bool:
        return (
            developer.is_following(self)
            and self.is_following(developer)
            and self._share_at_least_one_organization()
        )

    def is_following(self, developer: "Developer") -> bool:
        return True

    def _share_at_least_one_organization(self) -> bool:
        return True
