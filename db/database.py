from datetime import datetime
import sqlite3
import slots.slots as slots
from slots.slots import Slot as Slot


def init_db(db=None, leave_connection_open=False, file="db/database.db"):
    with open("schema.sql") as f:
        schema = f.read()

    with open("data.sql") as f:
        data = f.read()

    if not db:
        db = sqlite3.connect(file)
    cur = db.cursor()
    # enforce foreign key constraints
    cur.execute("PRAGMA foreign_keys = ON;")
    cur.executescript(schema)
    cur.executescript(data)
    db.commit()

    if not leave_connection_open:
        db.close()

    # print("Database initialized")


def reset_db(db=None, file="db/database.db", leave_connection_open=False):
    if not db:
        db = sqlite3.connect(file)
    cur = db.cursor()
    cur.execute("DROP TABLE IF EXISTS Termin;")
    cur.execute("DROP TABLE IF EXISTS BuergerBuero;")
    cur.execute("DROP TABLE IF EXISTS Stadt;")
    db.commit()
    if not leave_connection_open:
        db.close()


def save_slots_per_city(
    slots_to_be_saved: list[Slot],
    city: str,
    now=datetime.now(),
    db=None,
    leave_connection_open=False,
    debug=False,
):
    # print(f"Saving slots for {city} at {now}")
    result_dict = update_slots(
        slots_to_be_saved,
        timestamp=now,
        city=city,
        db=db,
        leave_connection_open=leave_connection_open,
        debug=debug,
    )

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

    currently_open = result_dict["currently_open"]
    updated = result_dict["updated"]
    all_open_slots_in_db = result_dict["all_open_slots_in_db"]
    new = result_dict["new"]
    inserted = result_dict["count_inserted"]
    ignored = result_dict["count_ignored"]

    log_string = f"{now} "
    log_string += f"{colors['warning']}{city}{colors['end']} - "
    log_string += f"{colors['blue']}Opn: {len(currently_open)}{colors['end']} "
    log_string += f"{colors['fail']}Up: {len(updated)}{colors['end']} "
    log_string += f"{colors['green']}New: {inserted}{colors['end']} "
    log_string += f"{colors['header']}Ign: {ignored}{colors['end']}"

    print(log_string)
    if not db:

        debug_log = f"{colors['header']}"
        debug_log += f"Inserted: {inserted} "
        debug_log += f"Ignored: {ignored}"
        debug_log += f"{colors['end']}"
        # print(debug_log)

    # slots.print_slots(open, "Open slots:")
    # slots.print_slots(updated, "Updated slots:", "fail")
    # slots.print_slots(new, "New slots:", "green")


def update_slots(
    current: list[Slot],
    city: str,
    timestamp=datetime.now(),
    db=None,
    leave_connection_open=False,
    debug=False,
):
    """
    updates the slots in the database with the current open slots

    open: list[Slot] - a list of all currently open slots
    city: str - the city of the slots to update
    timestamp: datetime - the timestamp of the update
    db: sqlite3.Connection - the database connection
    leave_connection_open: bool - if True, the connection to the database will not be closed

    returns a tuple of three lists:
    - open: all slots that are currently open
    - updated: all slots that were open, but are now closed
    - new: new slots that are now open, previously unknown
    """

    if isinstance(current, Slot):
        current = [current]

    if not db:
        db = sqlite3.connect("db/database.db")

    if debug:
        db.set_trace_callback(print)

    cur = db.cursor()

    # PRAGMA foreign_keys = ON;
    cur.execute("PRAGMA foreign_keys = ON;")

    queried_slots = cur.execute(
        """
        SELECT 
            Termin.buergerbuero, 
            Termin.datum, 
            Termin.angelegenheit
        FROM Termin
        INNER JOIN BuergerBuero ON Termin.buergerbuero = BuergerBuero.stadtteil
        WHERE Termin.erstmalsErfasstAlsBelegt IS NULL
        AND BuergerBuero.stadt = ?;
        """,
        (city,),
    ).fetchall()

    # tuple (office, date, concern) -> Slot
    all_open_slots_in_db = slots.create_slots(queried_slots)

    if debug:
        # print("All open slots in db:")
        for slot in queried_slots:
            # print(slot)
            created = slots.create_slots(slot)
            # print(created)

    updated = slots.difference(all_open_slots_in_db, current)

    # print(f"Updated slots: {updated}")

    # close all slots that are not in currently_open_slots
    cur.executemany(
        """
        UPDATE Termin
        SET erstmalsErfasstAlsBelegt = ?
        WHERE buergerbuero = ?
        AND datum = ?;
        """,
        [(timestamp, slot.office, slot.date) for slot in updated],
    )

    new = slots.difference(current, all_open_slots_in_db)

    if debug:
        debug_slots = slots.new_difference(current, all_open_slots_in_db)
        print("Count current:", len(current))
        print("Count all_open_slots_in_db:", len(all_open_slots_in_db))
        print("Count debug_slots:", len(debug_slots))
        print("Count new:", len(new))

    # Get the total changes before the insert operation
    total_changes_before = db.total_changes
    if not debug:
        cur.executemany(
            """
            INSERT OR IGNORE
            INTO Termin (buergerbuero, datum, angelegenheit, erstmalsErfasstAlsFrei)
            VALUES (?, ?, ?, ?);
            """,
            [(slot.office, slot.date, slot.concern, timestamp) for slot in new],
        )
    else:
        print("Would insert:")
        for slot in new:
            print(slot)

        cur.executemany(
            """
            INSERT
            INTO Termin (buergerbuero, datum, angelegenheit, erstmalsErfasstAlsFrei)
            VALUES (?, ?, ?, ?);
            """,
            [(slot.office, slot.date, slot.concern, timestamp) for slot in new],
        )

    db.commit()

    # Get the total changes after the insert operation
    total_changes_after = db.total_changes

    # Calculate the number of inserted rows
    inserted_rows = total_changes_after - total_changes_before

    # Calculate the number of ignored rows
    ignored_rows = len(new) - inserted_rows

    if not leave_connection_open:
        db.close()

    # return current, updated, new, all_open_slots_in_db

    return {
        "currently_open": current,
        "updated": updated,
        "new": new,
        "all_open_slots_in_db": all_open_slots_in_db,
        "count_inserted": inserted_rows,
        "count_ignored": ignored_rows,
    }
