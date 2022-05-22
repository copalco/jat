import unittest

from src.twitter.user import TwitterUser
from src.twitter.user_retriever import TwitterDevelopersRetriever


class TwitterDevelopersRetrieverTestCase(unittest.TestCase):
    def test_retrieves_connections_of_developers(self) -> None:
        user = TwitterDevelopersRetriever().user("copalco")
        self.assertEqual(TwitterUser(followed_by=[], following=[]), user)


if __name__ == "__main__":
    unittest.main()
