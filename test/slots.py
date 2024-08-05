from datetime import datetime
import unittest
import src.slots as slots
from src.slots import Slot as Slot


class TestSlots(unittest.TestCase):

    def test_difference_empty_when_same(self):

        A = [("Bürgerbüro 1", "2021-08-01 08:00:00")]
        B = [("Bürgerbüro 1", "2021-08-01 08:00:00")]

        self.assertEqual(slots.difference(A, B), [])
        print("When A and B are the same, the difference should be empty")

    def test_difference_empty_when_empty(self):

        A = []
        B = []

        self.assertEqual(slots.difference(A, B), [])
        print("When A and B are empty, the difference should be empty")

    def test_difference_not_empty_when_different(self):

        A = [("Bürgerbüro 1", "2021-08-01 08:00:00")]
        B = [("Bürgerbüro 2", "2021-08-01 08:00:00")]

        self.assertEqual(slots.difference(A, B), A)
        print("When A and B are different, the difference should be A")

    def test_date_format_equality(self):

        a = Slot("Bürgerbüro 1", "2021-08-01 08:00")
        b = Slot("Bürgerbüro 1", "2021-08-01 08:00:00")

        self.assertEqual(a, b)
        print("Slots with different date formats should be equal")

    def test_datetime_object_instanciation(self):

        a = Slot("Bürgerbüro 1", datetime(2021, 8, 1, 8, 0))
        b = Slot("Bürgerbüro 1", "2021-08-01 08:00:00")

        self.assertEqual(a, b)
        print("Datetime objects should be equal to date strings")

    def test_not_different_when_updated(self):

        a = Slot("Bürgerbüro 1", "2021-08-01 08:00:00")
        b = Slot("Bürgerbüro 1", "2021-08-01 08:00:00", updated="2021-08-01 08:01:00")

        A = [a]
        B = [b]

        print(
            "When A and B are the same, but B has an updated date, the difference should be empty"
        )
        self.assertEqual(slots.difference(A, B), [])

    def test_create_slots_from_2_tuple(self):

        A = [("Bürgerbüro 1", "2021-08-01 08:00:00")]
        B = [Slot("Bürgerbüro 1", "2021-08-01 08:00:00")]

        self.assertEqual(slots.create_slots(A), B)
        print("Slots should be created from a list of tuples")

    def test_create_slots_from_3_tuple(self):

        A = [("Bürgerbüro 1", "2021-08-01 08:00:00", "2021-08-01 08:01:00")]
        B = [Slot("Bürgerbüro 1", "2021-08-01 08:00:00", "2021-08-01 08:01:00")]

        self.assertEqual(slots.create_slots(A), B)
        print("Slots should be created from a list of tuples")

    def test_create_slots_from_4_tuple(self):

        A = [
            (
                "Bürgerbüro 1",
                "2021-08-01 08:00:00",
                "2021-08-01 08:01:00",
                "2021-08-01 08:02:00",
            )
        ]
        B = [
            Slot(
                "Bürgerbüro 1",
                "2021-08-01 08:00:00",
                "2021-08-01 08:01:00",
                "2021-08-01 08:02:00",
            )
        ]

        self.assertEqual(slots.create_slots(A), B)
        print("Slots should be created from a list of tuples")


if __name__ == "__main__":
    unittest.main()
