CREATE TABLE
    IF NOT EXISTS Slots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        office VARCHAR(255) NOT NULL,
        city VARCHAR(255) NOT NULL,
        timeslot DATE NOT NULL,
        concern VARCHAR(255) NOT NULL
    );

CREATE TABLE
    IF NOT EXISTS Availabilities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        slot_id INTEGER NOT NULL,
        available TIMESTAMP,
        taken TIMESTAMP,
        FOREIGN KEY (slot_id) REFERENCES Slots(id)
    );