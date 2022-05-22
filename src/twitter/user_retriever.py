import requests

from src.twitter.user import TwitterUser


class TwitterDevelopersRetriever:
    def __init__(self, api_token: str) -> None:
        self.api_token = api_token

    def user(self, username: str) -> TwitterUser:
        _ = requests.get(
            f"https://api.twitter.com/2/users/by/username/{username}",
            headers={"authorization": f"Bearer {self.api_token}"},
        )
        return TwitterUser(username, followed_by=[], following=[])
