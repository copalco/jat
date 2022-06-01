from dataclasses import dataclass

from src.domain.model.handle import Handle


@dataclass
class Developer:
    handle: Handle
    follows: list[Handle]
    organizations: list[str]

    def connected(self, developer: "Developer") -> bool:
        return (
            developer.is_following_on_twitter(self)
            and self.is_following_on_twitter(developer)
            and self._share_at_least_one_organization(developer)
        )

    def is_following_on_twitter(self, developer: "Developer") -> bool:
        return developer.handle in self.follows

    def _share_at_least_one_organization(self, developer: "Developer") -> bool:
        return bool(self.shared_organizations(developer))

    def shared_organizations(self, developer: "Developer") -> set[str]:
        return set(self.organizations).intersection(developer.organizations)
