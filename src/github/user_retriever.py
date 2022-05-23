from src.github.user import GithubUser


class GithubUserRetriever:
    def user(self, username: str) -> GithubUser:
        return GithubUser(username)
