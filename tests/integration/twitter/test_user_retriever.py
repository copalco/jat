import os
import unittest

from src.twitter.user import TwitterUser
from src.twitter.user_retriever import TwitterDevelopersRetriever


class TwitterDevelopersRetrieverTestCase(unittest.TestCase):
    def test_retrieves_connections_of_developers(self) -> None:
        user = TwitterDevelopersRetriever(api_token=os.environ["JAT_TWITTER_API_TOKEN"]).user(
            "copalco"
        )
        self.assertEqual(TwitterUser("copalco", followed_by=[], following=[]), user)


if __name__ == "__main__":
    unittest.main()
