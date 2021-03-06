import http

import requests
from requests.auth import HTTPBasicAuth

from src.github.user import GithubUser
from src.github.user_not_found import GithubUserNotFound


class GithubUserRetriever:
    def __init__(self, api_token: str) -> None:
        self.token = api_token

    def user(self, username: str) -> GithubUser:
        response = requests.get(
            f"https://api.github.com/users/{username}/orgs",
            auth=HTTPBasicAuth("copalco", self.token),
            headers={
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "copalco",
            },
        )
        if response.status_code == http.HTTPStatus.NOT_FOUND:
            raise GithubUserNotFound(username)
        raw_organizations = response.json()
        return GithubUser(
            username, organizations=[org["login"] for org in raw_organizations]
        )
