import requests

from src.twitter.user import TwitterUser


class TwitterDevelopersRetriever:
    def __init__(self, api_token: str) -> None:
        self.api_token = api_token

    def user(self, username: str) -> TwitterUser:
        response = requests.get(
            "https://api.twitter.com/2/users/by/username/{usesrname}",
            headers={"authorization": f"Bearer {self.api_token}"},
        )
        response.raise_for_status()
        return TwitterUser(username, followed_by=[], following=[])
