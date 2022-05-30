import unittest

from src.domain.model.developer import Developer
from src.domain.model.developer_not_found import DeveloperNotFound
from src.domain.model.handle import Handle
from src.github.user import GithubUser
from src.github.user_not_found import GithubUserNotFound
from src.github.user_retriever import GithubUserRetriever
from src.persistence.developers_repository import ExternalDevelopersRepository
from src.twitter.user import TwitterUser
from src.twitter.user_not_found import TwitterUserNotFound
from src.twitter.user_retriever import TwitterUsersRetriever


class FakeGithubRetriever(GithubUserRetriever):
    def __init__(self) -> None:
        self._users: dict[str, GithubUser] = {}
        super().__init__("")

    def add(self, user: GithubUser) -> None:
        self._users[user.username] = user

    def user(self, username: str) -> GithubUser:
        try:
            return self._users[username]
        except KeyError:
            raise GithubUserNotFound()


class FakeTwitterRetriever(TwitterUsersRetriever):
    def __init__(self) -> None:
        self._users: dict[str, TwitterUser] = {}
        super().__init__("")

    def add(self, user: TwitterUser) -> None:
        self._users[user.username] = user

    def user(self, username: str) -> TwitterUser:
        try:
            return self._users[username]
        except KeyError:
            raise TwitterUserNotFound()


class ExternalDevelopersRepositoryTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.twitter_retriever = FakeTwitterRetriever()  # type: ignore
        self.github_retriever = FakeGithubRetriever()  # type: ignore

    def test_retrieves_user_from_guthub_and_twitter_retrievers(self) -> None:
        repository = ExternalDevelopersRepository(
            self.twitter_retriever, self.github_retriever
        )
        self.twitter_retriever.add(TwitterUser("dev1", follows=["dev2", "dev5"]))
        self.github_retriever.add(
            GithubUser("dev1", organizations=["org1", "org2", "org3"])
        )
        developer = repository.get(Handle("dev1"))
        self.assertEqual(
            Developer(
                Handle("dev1"),
                follows=[Handle("dev2"), Handle("dev5")],
                organizations=["org1", "org2", "org3"],
            ),
            developer,
        )

    def test_returns_developer_error_if_user_is_not_present_in_any_service(
        self,
    ) -> None:
        repository = ExternalDevelopersRepository(
            self.twitter_retriever, self.github_retriever
        )
        with self.assertRaises(DeveloperNotFound) as exception_info:
            _ = repository.get(Handle("dev1"))
        self.assertEqual(
            DeveloperNotFound(Handle("dev1"), ["twitter", "github"]),
            exception_info.exception,
            exception_info.exception.args,
        )
