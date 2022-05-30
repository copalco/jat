from typing import TypedDict

import requests

from src.twitter.user import TwitterUser
from src.twitter.user_not_found import TwitterUserNotFound


class RawUser(TypedDict):
    id: str
    name: str
    username: str


class TwitterUsersRetriever:
    def __init__(self, api_token: str) -> None:
        self.api_token = api_token

    def user(self, username: str) -> TwitterUser:
        user = self._user(username)
        followers = self._followed_by(user)
        follows = self._follows(user)
        return TwitterUser(
            username,
            follows=follows,
        )

    def _followed_by(self, user: RawUser) -> list[str]:
        return []

    def _follows(self, user: RawUser) -> list[str]:
        followers_response = requests.get(
            f"https://api.twitter.com/2/users/{user['id']}/following?max_results=1000",
            headers={"authorization": f"Bearer {self.api_token}"},
        )
        raw_followers = followers_response.json()["data"]
        followers = [follower["username"] for follower in raw_followers]
        next_token = followers_response.json()["meta"].get("next_token")
        if next_token:
            followers_response = requests.get(
                f"https://api.twitter.com/2/users/{user['id']}/following?max_results=1000",
                headers={"authorization": f"Bearer {self.api_token}"},
            )
            raw_followers = followers_response.json()["data"]
            followers.extend(follower["username"] for follower in raw_followers)
        return followers

    def _user(self, username: str) -> RawUser:
        serialized_user_response = requests.get(
            f"https://api.twitter.com/2/users/by/username/{username}",
            headers={"authorization": f"Bearer {self.api_token}"},
        )
        user_response = serialized_user_response.json()
        if (
            "errors" in user_response
            and user_response["errors"][0]["title"] == "Not Found Error"
        ):
            raise TwitterUserNotFound(username)
        raw_user = user_response["data"]
        return raw_user
