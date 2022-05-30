from src.domain.model.developer import Developer
from src.domain.model.handle import Handle
from src.github.user_retriever import GithubUserRetriever
from src.twitter.user_retriever import TwitterUsersRetriever


class DevelopersRepository:
    def __init__(
        self,
        twitter_retriever: TwitterUsersRetriever,
        github_retriever: GithubUserRetriever,
    ) -> None:
        self._twitter_retriever = twitter_retriever
        self._github_retriever = github_retriever

    def get(self, handle: Handle) -> Developer:
        return Developer(handle, follows=[], followed_by=[], organizations=[])
