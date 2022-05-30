import unittest

from src.developers.developers_repository import DevelopersRepository
from src.domain.model.developer import Developer
from src.domain.model.handle import Handle
from src.github.user import GithubUser
from src.github.user_retriever import GithubUserRetriever
from src.twitter.user import TwitterUser
from src.twitter.user_retriever import TwitterUsersRetriever


class FakeGithubRetriever(GithubUserRetriever):
    def __init__(self) -> None:
        self._users: dict[str, GithubUser] = {}
        super().__init__("")

    def add(self, user: GithubUser) -> None:
        self._users[user.username] = user

    def user(self, username: str) -> GithubUser:
        return self._users[username]


class FakeTwitterRetriever(TwitterUsersRetriever):
    def __init__(self) -> None:
        self._users: dict[str, TwitterUser] = {}
        super().__init__("")

    def add(self, user: TwitterUser) -> None:
        self._users[user.username] = user

    def user(self, username: str) -> TwitterUser:
        return self._users[username]


class DevelopersRepositoryTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.twitter_retriever = FakeTwitterRetriever()  # type: ignore
        self.github_retriever = FakeGithubRetriever()  # type: ignore

    def test_retrieves_user_from_guthub_and_twitter_retrievers(self) -> None:
        repository = DevelopersRepository(self.twitter_retriever, self.github_retriever)
        self.twitter_retriever.add(
            TwitterUser(
                "dev1", followed_by=["dev2", "dev3"], following=["dev2", "dev5"]
            )
        )
        developer = repository.get(Handle("dev1"))
        self.assertEqual(
            Developer(
                Handle("dev1"),
                follows=[Handle("dev2"), Handle("dev5")],
                followed_by=[Handle("dev2"), Handle("dev3")],
                organizations=[],
            ),
            developer,
        )
