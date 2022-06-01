import datetime
import unittest

import freezegun

from src.domain.events.events import DevelopersAreConnected, DevelopersAreNotConnected
from src.domain.model.connection import Connection
from src.domain.model.connection_id import ConnectionId
from src.domain.model.developer import Developer
from src.domain.model.handle import Handle


class ConnectionTestCase(unittest.TestCase):
    def test_registers_not_connected_event_if_developers_are_not_connected(self):
        first_handle = Handle("dev1")
        developer1 = Developer(
            first_handle,
            follows=[Handle("dev3")],
            organizations=["a", "b", "c"],
        )
        second_handle = Handle("dev2")
        developer2 = Developer(
            second_handle,
            follows=[Handle("dev3")],
            organizations=["a", "z"],
        )
        with freezegun.freeze_time("2022-05-30"):
            connection = Connection(
                ConnectionId.from_handles(first_handle, second_handle)
            )
            connection.register(developer1, developer2)
        self.assertEqual(
            [
                DevelopersAreNotConnected(
                    handles=(first_handle, second_handle),
                    registered_at=datetime.datetime(2022, 5, 30),
                )
            ],
            connection.changes(),
        )

    def test_registers_connected_event_if_developers_are_connected(self):
        first_handle = Handle("dev1")
        second_handle = Handle("dev2")
        developer1 = Developer(
            first_handle,
            follows=[second_handle],
            organizations=["a", "b", "c"],
        )
        developer2 = Developer(
            second_handle,
            follows=[first_handle],
            organizations=["a", "z"],
        )
        with freezegun.freeze_time("2022-05-30"):
            connection = Connection(
                ConnectionId.from_handles(first_handle, second_handle)
            )
            connection.register(developer1, developer2)
        self.assertEqual(
            [
                DevelopersAreConnected(
                    handles=(first_handle, second_handle),
                    registered_at=datetime.datetime(2022, 5, 30),
                    organizations={"a"},
                )
            ],
            connection.changes(),
        )
