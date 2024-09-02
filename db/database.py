from datetime import datetime
import sqlite3
import slots.slots as slots
from slots.slots import Slot as Slot


def init_db(db=None, leave_connection_open=False, reset=False, file="db/database.db"):

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
    slots: list[Slot],
    city: str,
    now=datetime.now(),
    db=None,
    leave_connection_open=False,
):
    # print(f"Saving slots for {city} at {now}")
    open, updated, new = update_slots(slots, timestamp=now, city=city)

    # slots.print_slots(open, "Open slots:")
    # slots.print_slots(updated, "Updated slots:", "fail")
    # slots.print_slots(new, "New slots:", "green")

    print(
        f"Open: {len(open)} Updated: {len(updated)} New: {len(new)} in {city} at {now}"
    )


def update_slots(
    open: list[Slot],
    city: str,
    timestamp=datetime.now(),
    db=None,
    leave_connection_open=False,
) -> tuple[list[Slot], list[Slot], list[Slot]]:
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

    if isinstance(open, Slot):
        open = [open]

    if not db:
        db = sqlite3.connect("db/database.db")

    cur = db.cursor()

    all_open_slots_in_db = cur.execute(
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
    all_open_slots_in_db = slots.create_slots(all_open_slots_in_db)

    updated = slots.difference(all_open_slots_in_db, open)
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

    new = slots.difference(open, all_open_slots_in_db)

    # save all slots, that are in currently_open_slots, but not in db
    cur.executemany(
        """
        INSERT OR IGNORE
        INTO Termin (buergerbuero, datum, angelegenheit, erstmalsErfasstAlsFrei)
        VALUES (?, ?, ?, ?);
        """,
        [(slot.office, slot.date, slot.concern, timestamp) for slot in new],
    )

    db.commit()

    if not leave_connection_open:
        db.close()

    return (open, updated, new)
