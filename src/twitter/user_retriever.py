import requests

from src.twitter.user import TwitterUser


class TwitterDevelopersRetriever:
    def __init__(self, api_token: str) -> None:
        self.api_token = api_token

    def user(self, username: str) -> TwitterUser:
        user_response = requests.get(
            f"https://api.twitter.com/2/users/by/username/{username}",
            headers={"authorization": f"Bearer {self.api_token}"},
        )
        raw_user = user_response.json()["data"]
        followers_response = requests.get(
            f"https://api.twitter.com/2/users/{raw_user['id']}/followers",
            headers={"authorization": f"Bearer {self.api_token}"},
        )
        raw_followers = followers_response.json()["data"]
        following_response = requests.get(
            f"https://api.twitter.com/2/users/{raw_user['id']}/followers",
            headers={"authorization": f"Bearer {self.api_token}"},
        )
        raw_following = following_response.json()["data"]
        return TwitterUser(
            username,
            followed_by=[follower["username"] for follower in raw_followers],
            following=[following["username"] for following in raw_following],
        )
