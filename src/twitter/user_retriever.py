import requests

from src.twitter.user import TwitterUser
from src.twitter.user_not_found import TwitterUserNotFound


class TwitterUsersRetriever:
    def __init__(self, api_token: str) -> None:
        self.api_token = api_token

    def user(self, username: str) -> TwitterUser:
        user = self._user(username)
        followers = self._followers_of(user)
        following = self._followed_by(user)
        return TwitterUser(
            username,
            followed_by=followers,
            following=following,
        )

    def _followed_by(self, user):
        following_response = requests.get(
            f"https://api.twitter.com/2/users/{user['id']}/followers",
            headers={"authorization": f"Bearer {self.api_token}"},
        )
        raw_following = following_response.json()["data"]
        following = [following["username"] for following in raw_following]
        return following

    def _followers_of(self, raw_user):
        followers_response = requests.get(
            f"https://api.twitter.com/2/users/{raw_user['id']}/followers",
            headers={"authorization": f"Bearer {self.api_token}"},
        )
        raw_followers = followers_response.json()["data"]
        followers = [follower["username"] for follower in raw_followers]
        return followers

    def _user(self, username):
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
