import os
import unittest

from src.github.user import GithubUser
from src.github.user_retriever import GithubUserRetriever


class GithubUserRetrieverTestCase(unittest.TestCase):
    def test_retrieves_user_github_user(self):
        user = GithubUserRetriever(os.environ["JAT_GITHUB_API_TOKEN"]).user(
            username="defunkt"
        )
        self.assertEqual(
            GithubUser("defunkt"),
            user,
            user,
        )
