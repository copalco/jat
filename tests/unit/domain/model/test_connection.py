import datetime
import unittest

import freezegun

from src.domain.events.events import DevelopersAreConnected, DevelopersAreNotConnected
from src.domain.model.connection import Connection
from src.domain.model.developer import Developer
from src.domain.model.handle import Handle


class ConnectionTestCase(unittest.TestCase):
    def test_registers_not_connected_event_if_developers_are_not_connected(self):
        developer1 = Developer(
            Handle("dev1"),
            follows=[Handle("dev3")],
            followed_by=[Handle("dev0")],
            organizations=["a", "b", "c"],
        )
        developer2 = Developer(
            Handle("dev2"),
            follows=[Handle("dev3")],
            followed_by=[Handle("dev5")],
            organizations=["a", "z"],
        )
        with freezegun.freeze_time("2022-05-30"):
            connection = Connection.register(developer1, developer2)
        self.assertEqual(
            [
                DevelopersAreNotConnected(
                    handles=(Handle("dev1"), Handle("dev2")),
                    registered_at=datetime.datetime(2022, 5, 30),
                )
            ],
            connection.changes(),
        )

    def test_registers_connected_event_if_developers_are_connected(self):
        developer1 = Developer(
            Handle("dev1"),
            follows=[Handle("dev2")],
            followed_by=[Handle("dev2")],
            organizations=["a", "b", "c"],
        )
        developer2 = Developer(
            Handle("dev2"),
            follows=[Handle("dev1")],
            followed_by=[Handle("dev1")],
            organizations=["a", "z"],
        )
        with freezegun.freeze_time("2022-05-30"):
            connection = Connection.register(developer1, developer2)
        self.assertEqual(
            [
                DevelopersAreConnected(
                    handles=(Handle("dev1"), Handle("dev2")),
                    registered_at=datetime.datetime(2022, 5, 30),
                    organizations={"a"},
                )
            ],
            connection.changes(),
        )
