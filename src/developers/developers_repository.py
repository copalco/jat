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
        twitter_user = self._twitter_retriever.user(str(handle))
        return Developer(
            handle,
            follows=[Handle(tu) for tu in twitter_user.following],
            followed_by=[Handle(tu) for tu in twitter_user.followed_by],
            organizations=[],
        )
