import unittest

from src.domain.model.developer import Developer
from src.domain.model.handle import Handle


class DeveloperTestCase(unittest.TestCase):
    def test_developers_are_connected(self):
        developer1 = Developer(Handle("dev1"), organizations=["a", "b", "c"])
        developer2 = Developer(Handle("dev2"), organizations=["a", "x", "c", "z"])
        self.assertTrue(developer1.connected(developer2))
