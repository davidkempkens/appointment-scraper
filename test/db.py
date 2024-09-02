import os
import sqlite3
import unittest
import db.database as db
import slots.slots as slots
from slots.slots import Slot as Slot


class TestDatabase(unittest.TestCase):

    def setUp(self):
        db_file = "file:mem1?mode=memory&cache=shared"
        # create database
        self.db = sqlite3.connect(db_file, uri=True)
        # db.reset_db(db=self.db, leave_connection_open=True)
        db.init_db(db=self.db, leave_connection_open=True)
        # set tracebacks
        # self.db.set_trace_callback(print)

    def test_first_time_slot_not_in_updated(self):

        # create Test Slots
        a = Slot("Bilk", "2021-08-01 08:00:00")

        # insert new slot via update_slots
        open, updated, new = db.update_slots(a, db=self.db, city="Duesseldorf")

        # check if the slot is not in the updated slots
        self.assertNotIn(a, updated)
        print(
            "New slots should not be in the updated slots, the first time they are inserted"
        )

    def test_new_slot_in_new_slots(self):

        # create Test Slots
        a = Slot("Bilk", "2021-08-01 08:00:00")

        # insert new slot via update_slots
        open, updated, new = db.update_slots(a, db=self.db, city="Duesseldorf")

        # check if the slot is not in the new slots
        self.assertIn(a, new)
        print("New slots should be in the new slots, the first time they are inserted")

    def test_open_slot_found_the_second_time(self):

        # create Test Slots
        a = Slot("Bilk", "2021-08-01 08:00:00")

        # insert new slot via update_slots
        open, updated, new = db.update_slots(
            a, db=self.db, leave_connection_open=True, city="Duesseldorf"
        )

        # insert the same slot again
        open, updated, new = db.update_slots(a, db=self.db, city="Duesseldorf")

        # check if the slot is in the updated slots
        self.assertNotIn(a, updated)
        print(
            "Open slots should not be in the updated slots, the second time they found"
        )

    def test_open_slot_not_in_new_slots(self):

        # create Test Slots
        a = Slot("Bilk", "2021-08-01 08:00:00")

        # insert new slot via update_slots
        open, updated, new = db.update_slots(
            a, db=self.db, leave_connection_open=True, city="Duesseldorf"
        )

        # insert the same slot again
        open, updated, new = db.update_slots(a, db=self.db, city="Duesseldorf")

        # check if the slot is not in the new slots
        self.assertNotIn(a, new)
        print("Open slots should not be in the new slots, the second time they found")

    def test_open_slot_in_open_slots_the_second_time(self):

        # create Test Slots
        a = Slot("Bilk", "2021-08-01 08:00:00")

        # insert new slot via update_slots
        open, updated, new = db.update_slots(
            a, db=self.db, leave_connection_open=True, city="Duesseldorf"
        )

        # insert the same slot again
        open, updated, new = db.update_slots(a, db=self.db, city="Duesseldorf")

        # check if the slot is in the open slots
        self.assertIn(a, open)
        print("Open slots should be in the open slots, the second time they are found")

    def test_open_slot_in_db_not_found_this_time(self):

        # create Test Slots
        a = Slot("Bilk", "2021-08-01 08:00:00")

        b = Slot("Bilk", "2021-08-01 09:00:00")

        # insert new slot via update_slots
        open, updated, new = db.update_slots(
            a, db=self.db, leave_connection_open=True, city="Duesseldorf"
        )

        # insert a different slot
        open, updated, new = db.update_slots(b, db=self.db, city="Duesseldorf")

        # check if the slot is not in the db
        self.assertNotIn(a, open)

    def test_different_city_doesnt_get_updated(self):

        # create Test Slots
        open_slot_in_duesseldorf = Slot("Bilk", "2021-08-01 08:00:00")

        open_slot_in_bremen = Slot("BuergerServiceCenter-Mitte", "2021-08-01 08:00:00")

        # insert new slot via update_slots
        open, updated, new = db.update_slots(
            open_slot_in_duesseldorf,
            db=self.db,
            leave_connection_open=True,
            city="Duesseldorf",
        )

        # insert a different slot
        open, updated, new = db.update_slots(
            open_slot_in_bremen,
            db=self.db,
            city="Bremen",
        )

        # check if the slot in duesseldorf is not in the updated slots

        self.assertNotIn(open_slot_in_duesseldorf, updated)
        print("Open slots in different cities should not be updated")


if __name__ == "__main__":
    unittest.main()
