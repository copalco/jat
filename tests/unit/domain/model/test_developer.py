import unittest

from src.domain.model.developer import Developer
from src.domain.model.handle import Handle


class DeveloperTestCase(unittest.TestCase):
    def test_developers_are_connected(self) -> None:
        developer1 = Developer(
            Handle("dev1"),
            follows=[Handle("dev3"), Handle("dev2")],
            organizations=["a", "b", "c"],
        )
        developer2 = Developer(
            Handle("dev2"),
            follows=[Handle("dev1")],
            organizations=["a", "x", "c", "z"],
        )
        self.assertTrue(developer1.connected(developer2))

    def test_are_not_connected_if_do_not_share_organization(self) -> None:
        developer1 = Developer(
            Handle("dev1"),
            follows=[Handle("dev2")],
            organizations=["a", "b", "c"],
        )
        developer2 = Developer(
            Handle("dev2"),
            follows=[Handle("dev1")],
            organizations=["x", "z"],
        )
        self.assertFalse(developer1.connected(developer2))

    def test_are_not_connected_if_do_not_follow_each_other(self) -> None:
        developer1 = Developer(
            Handle("dev1"),
            follows=[Handle("dev3")],
            organizations=["a", "b", "c"],
        )
        developer2 = Developer(
            Handle("dev2"),
            follows=[Handle("dev1")],
            organizations=["a", "z"],
        )
        self.assertFalse(developer1.connected(developer2))
