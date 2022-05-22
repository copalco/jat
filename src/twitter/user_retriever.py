from src.twitter.user import TwitterUser


class TwitterDevelopersRetriever:
    def user(self, username: str) -> TwitterUser:
        return TwitterUser(username, followed_by=[], following=[])
