import unittest

from requests import HTTPError

from src.twitter.user_retriever import TwitterDevelopersRetriever


class TwitterDevelopersRetrieverTestCase(unittest.TestCase):
    def test_retrieves_connections_of_developers(self) -> None:
        with self.assertRaises(HTTPError) as exception_info:
            TwitterDevelopersRetriever(api_token="test").user("copalco")
        self.assertEqual(exception_info.exception.response.status_code, 401)


if __name__ == "__main__":
    unittest.main()
