import requests
from requests.auth import HTTPBasicAuth

from src.github.user import GithubUser


class GithubUserRetriever:
    def __init__(self, api_token: str) -> None:
        self.token = api_token

    def user(self, username: str) -> GithubUser:
        _ = requests.get(
            f"https://api.github.com/users/{username}/orgs",
            auth=HTTPBasicAuth("copalco", self.token),
            headers={
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "copalco",
            },
        )
        return GithubUser(username)
