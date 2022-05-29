import unittest

from src.domain.model.handle import Handle


class HandleTestCase(unittest.TestCase):
    def test_is_hashable(self) -> None:
        self.assertEqual(hash(Handle("test")), hash("test"))

    def test_handles_are_equal(self) -> None:
        self.assertEqual(Handle("test"), Handle("test"))

    def test_handle_to_string_is_its_value(self) -> None:
        self.assertEqual(str(Handle("test")), "test")

    def test_handle_can_only_be_compared_with_other_handle(self) -> None:
        class SomethingElse:
            value = "test"

        self.assertNotEqual(Handle("test"), SomethingElse())

    def test_handle_cannot_be_longer_than_15_characters(self) -> None:
        with self.assertRaises(ValueError) as exception_info:
            _ = Handle("test1" * 3 + "1")
        self.assertEqual(
            str(exception_info.exception), "Handle can have up to 15 characters"
        )

    def test_handle_cannot_be_shorter_than_4_characters(self) -> None:
        with self.assertRaises(ValueError) as exception_info:
            _ = Handle("tes")
        self.assertEqual(
            str(exception_info.exception), "Handle must have at least 4 characters"
        )
