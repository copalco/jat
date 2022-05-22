import unittest

from src.github.user import GithubUser
from src.github.user_retriever import GithubUserRetriever


class GithubUserRetrieverTestCase(unittest.TestCase):
    def test_retrieves_user_github_user(self):
        self.assertEqual(GithubUser(), GithubUserRetriever().user(username="copalco"))
