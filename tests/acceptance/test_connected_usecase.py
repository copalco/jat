import random
import unittest

import requests

API_URL = "http://localhost:8080"


class ConnectedTestCase(unittest.TestCase):
    def test_developers_which_are_connected(self) -> None:
        seed = random.randint(0, 9999999)
        first_developer_handle = f"test_{seed}"
        second_developer_handle = f"test_2_{seed}"
        organisation = f"org_{seed}"
        self.create_developer_on_twitter(first_developer_handle)
        self.create_developer_on_twitter(second_developer_handle)
        self.make_developers_follow_each_other(
            first_developer_handle, second_developer_handle
        )
        self.create_organisation_on_github(organisation)
        self.create_developer_on_github(first_developer_handle)
        self.create_developer_on_github(second_developer_handle)
        self.add_developers_to_organisation(
            first_developer_handle, second_developer_handle, organisation
        )
        self.assert_that_developers_are_connected(
            first_developer_handle, second_developer_handle, organisation
        )

    def create_developer_on_twitter(self, developer_handle: str) -> None:
        pass

    def make_developers_follow_each_other(
        self, first_developer_handle: str, second_developer_handle: str
    ) -> None:
        pass

    def create_developer_on_github(self, developer_handle: str) -> None:
        pass

    def create_organisation_on_github(self, name: str) -> None:
        pass

    def add_developers_to_organisation(
        self,
        first_developer_handle: str,
        second_developer_handle: str,
        organization: str,
    ) -> None:
        pass

    def assert_that_developers_are_connected(
        self,
        first_developer_handle: str,
        second_developer_handle: str,
        organization: str,
    ) -> None:
        response = requests.get(
            f"{API_URL}/connected/realtime/{first_developer_handle}/{second_developer_handle}"
        )

        self.assertEqual(response.json(), {"connected": True, "organizations": []})
