from src.twitter.user import TwitterUser


class TwitterDevelopersRetriever:
    def __init__(self, api_token: str) -> None:
        self.api_token = api_token

    def user(self, username: str) -> TwitterUser:
        return TwitterUser(username, followed_by=[], following=[])
