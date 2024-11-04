from datetime import datetime
import sqlite3

from model.Slot import Slot


class SlotRepository:
    def __init__(self, db=sqlite3.connect("db/database.db")):
        self.db = db
        self.cur = db.cursor()
        self.cur.execute("PRAGMA foreign_keys = ON;")

    def initCities(self, cities):
        for city in cities:
            print(f"Initializing city: {city}")
            self.db = sqlite3.connect(f"db/{city}.db")
            self.reset_db(keep_connection=True)

    def reset_db(self, keep_connection=False):

        # print sql commands
        self.db.set_trace_callback(print)

        # drop tables
        self.cur.execute("DROP TABLE IF EXISTS Availabilities;")
        self.cur.execute("DROP TABLE IF EXISTS Slots;")

        # create tables
        with open("schema.sql") as f:
            schema = f.read()
            self.cur.executescript(schema)

        if not keep_connection:
            self.__commit_and_close()

    def __commit_and_close(self):
        self.db.commit()
        self.db.close()

    def synchronize_slots(self, online_slots, city, concern, debug=False):

        if debug:
            self.db.set_trace_callback(print)

        # print(f"Syncing slots for {city} with concern {concern}")

        # get all slots from Slots WITH THE SAME CITY AND CONCERN
        #  where the Availabilities.slot_id matches the Slots.id
        # and the slot is still available
        open_db_slots = self.cur.execute(
            """
            SELECT Slots.id, Slots.office, Slots.city, Slots.timeslot, Slots.concern
            FROM Slots
            WHERE id IN (
                SELECT slot_id FROM Availabilities WHERE taken IS NULL
            )
            AND Slots.city = ?
            AND Slots.concern = ?;
            """,
            (city, concern),
        ).fetchall()

        open_db_slots = [Slot.make_from_db(slot) for slot in open_db_slots]

        updated_slots = []

        # check for every slot in the db with this concern and city
        # if it is still available online
        for open_db_slot in open_db_slots:

            # check if the db-slot is still available in the online-slots
            for online_slot in online_slots:

                if (
                    open_db_slot.office == online_slot.office
                    and open_db_slot.city == online_slot.city
                    and open_db_slot.timeslot == online_slot.timeslot
                    and open_db_slot.concern == online_slot.concern
                ):
                    # if the slot is still available online, break
                    # this db-slot is still available and does not need to be updated
                    break

                # if the db-slot is not available online anymore, update it
            else:
                # set the slot as taken in the db if it is not available online anymore
                # but only if the slot has the same city and concern
                # if open_db_slot.city == city and open_db_slot.concern == concern:
                self.__update_slot_as_taken(open_db_slot.id, datetime.now())
                # print(f"Updated slot as taken: {open_db_slot}")
                updated_slots.append(open_db_slot)

        # new online slots that are not in the db
        newly_available_slots_online_not_in_open_db = []

        for online_slot in online_slots:

            for open_db_slot in open_db_slots:

                if (
                    open_db_slot.office == online_slot.office
                    and open_db_slot.city == online_slot.city
                    and open_db_slot.timeslot == online_slot.timeslot
                    and open_db_slot.concern == online_slot.concern
                ):
                    break
            else:
                newly_available_slots_online_not_in_open_db.append(online_slot)

        newly_inserted_availabilities = self.__insert_new_slots_to_db(
            newly_available_slots_online_not_in_open_db
        )

        self.__commit_and_close()

        return {
            "online": online_slots,
            "db": open_db_slots,
            "updated": updated_slots,
            "new": newly_inserted_availabilities,
        }

    def print(self, report, city, concern, verbose=False):

        colors = {
            "header": "\033[95m",
            "blue": "\033[94m",
            "green": "\033[92m",
            "warning": "\033[93m",
            "fail": "\033[91m",
            "end": "\033[0m",
            "bold": "\033[1m",
            "underline": "\033[4m",
            None: "",
        }

        now = datetime.now().strftime("%H:%M")

        log_string = f"{now} "
        log_string += f"{colors['warning']}{city}{colors['end']} {concern} "
        log_string += f"{colors['blue']}{len(report['online'])}{colors['end']} = "
        log_string += f"{colors['header']}{len(report['db'])}{colors['end']} - "
        log_string += f"{colors['fail']}{len(report['updated'])}{colors['end']} + "
        log_string += f"{colors['green']}{len(report['new'])}{colors['end']}"

        plausibility = len(report["db"]) - len(report["updated"]) + len(
            report["new"]
        ) == len(report["online"])

        if not plausibility:
            log_string += f" {colors['fail']}X{colors['end']}"
        # else:
            # log_string += f" {colors['green']}\u2713{colors['end']}"

        print(log_string)

        if verbose:
            print(f"Syncing slots for {city} with concern {concern} at {now}")

            print(f"{colors['blue']}Online:")
            for slot in report["online"]:
                print(slot)

            print(f"{colors['header']}DB:")
            for slot in report["db"]:
                print(slot)

            print(f"{colors['fail']}Updated:")
            for slot in report["updated"]:
                print(slot)

            print(f"{colors['green']}New:")
            for slot in report["new"]:
                print(slot)

            print(f"{colors['end']}")
            print(f"Plausibility: {plausibility}")
            print(log_string)

    def __insert_new_slots_to_db(self, newly_available_slots_online):

        for slot in newly_available_slots_online:

            id_for_slot = None

            # check if the slot is already in the db
            already_in_db = self.cur.execute(
                """
                SELECT * FROM Slots
                WHERE office=? AND city=? AND timeslot=? AND concern=?;
                """,
                (slot.office, slot.city, slot.timeslot, slot.concern),
            ).fetchall()

            # check if empty
            if already_in_db:
                # print(f"Slot already in db: {slot}")

                if len(already_in_db) > 1:
                    raise Exception("Slot is in db multiple times")

                if len(already_in_db) == 1:
                    id_for_slot = already_in_db[0][0]

            elif not already_in_db:
                # print(f"Slot not in db: {slot}")

                id_for_slot = self.cur.execute(
                    """
                    INSERT INTO Slots (office, city, timeslot, concern)
                    VALUES (?, ?, ?, ?) RETURNING id;
                    """,
                    (slot.office, slot.city, slot.timeslot, slot.concern),
                ).fetchone()[0]
                # inserted_id = self.cur.fetchone()[0]
                # print(f"Inserted slot with id: {id_for_slot}")

            slot.id = id_for_slot
            # print(f"Slot with id: {id_for_slot}")

            # get all availabilities for this slot_id
            already_available = self.cur.execute(
                """
                SELECT * FROM Availabilities
                WHERE slot_id=? AND taken IS NULL;
                """,
                (id_for_slot,),
            ).fetchall()

            # print(f"len(already_available): {len(already_available)}")

            # when there is no availability for this slot_id, insert one
            if not already_available:
                avail_id = self.__insert_as_available(id_for_slot, datetime.now())
                # print(f"Inserted availability with id: {avail_id}")
        return newly_available_slots_online
        # self.commit_and_close()

    def __insert_as_available(self, slot_id, timestamp):
        return self.cur.execute(
            """
            INSERT INTO Availabilities (slot_id, available)
            VALUES (?, ?) RETURNING *;
            """,
            (slot_id, timestamp),
        ).fetchone()

    def __update_slot_as_taken(self, slot_id, timestamp):

        # get all availabilities for this slot_id
        availabilities_for_slot = self.cur.execute(
            "SELECT * FROM Availabilities WHERE slot_id=?", (slot_id,)
        ).fetchall()

        # check if empty
        if not availabilities_for_slot:
            raise Exception(
                "Slot can't be set as taken, because it was never available"
            )

        # save the current timestamp in the column "taken",
        # where the "available" timestamp is the latest
        return self.cur.execute(
            """
            UPDATE Availabilities
            SET taken = ?
            WHERE slot_id = ?
            AND available = (SELECT MAX(available) FROM Availabilities WHERE slot_id=?);
            """,
            (timestamp, slot_id, slot_id),
        ).fetchone()
