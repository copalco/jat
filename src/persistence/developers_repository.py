from src.domain.model.developer import Developer
from src.domain.model.developer_not_found import DeveloperNotFound
from src.domain.model.developers_repository import DevelopersRepository
from src.domain.model.handle import Handle
from src.github.user import GithubUser
from src.github.user_retriever import GithubUserRetriever
from src.twitter.user import TwitterUser
from src.twitter.user_not_found import TwitterUserNotFound
from src.twitter.user_retriever import TwitterUsersRetriever


class ExternalDevelopersRepository(DevelopersRepository):
    def __init__(
        self,
        twitter_retriever: TwitterUsersRetriever,
        github_retriever: GithubUserRetriever,
    ) -> None:
        self._twitter_retriever = twitter_retriever
        self._github_retriever = github_retriever

    def get(self, handle: Handle) -> Developer:
        absent_on: list[str] = []
        twitter_user: TwitterUser | None = None
        github_user: GithubUser | None = None
        try:
            twitter_user = self._twitter_retriever.user(str(handle))
        except TwitterUserNotFound:
            absent_on.append("twitter")
        try:
            github_user = self._github_retriever.user(str(handle))
        except:
            absent_on.append("github")
        if absent_on:
            raise DeveloperNotFound(handle, absent_on)
        if not twitter_user or not github_user:
            raise RuntimeError("Impossible!")
        return Developer(
            handle,
            follows=[Handle(tu) for tu in twitter_user.follows],
            organizations=github_user.organizations,
        )
