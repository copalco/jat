import os
import unittest

from src.github.user import GithubUser
from src.github.user_not_found import GithubUserNotFound
from src.github.user_retriever import GithubUserRetriever


class GithubUserRetrieverTestCase(unittest.TestCase):
    def test_retrieves_github_user(self):
        user = GithubUserRetriever(os.environ["JAT_GITHUB_API_TOKEN"]).user(
            username="defunkt"
        )
        self.assertEqual(
            GithubUser("defunkt", ["mustache"]),
            user,
            user,
        )

    def test_returns_no_such_user_on_not_found(self):
        with self.assertRaises(GithubUserNotFound):
            _ = GithubUserRetriever(os.environ["JAT_GITHUB_API_TOKEN"]).user(
                username="usernameofnotexistinguser1234432156788765"
            )
