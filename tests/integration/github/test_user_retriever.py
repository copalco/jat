import unittest

from src.github.user_retriever import GithubUserRetriever


class GithubUserRetrieverTestCase(unittest.TestCase):
    def test_retrieves_user_github_user(self):
        self.assertEqual(
            {
                "documentation_url": "https://docs.github.com/rest/reference/orgs#list-organizations-for-a-user",
                "message": "Not Found",
            },
            GithubUserRetriever().user(username="copalco"),
        )
