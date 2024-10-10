CREATE TABLE
    IF NOT EXISTS Slot (
        id INT AUTO_INCREMENT PRIMARY KEY,
        office VARCHAR(255) NOT NULL,
        city VARCHAR(255) NOT NULL,
        timeslot DATE NOT NULL,
        concern VARCHAR(255) NOT NULL
    );

CREATE TABLE
    IF NOT EXISTS Availabilities (
        id INT AUTO_INCREMENT PRIMARY KEY,
        slot_id INT NOT NULL,
        available TIMESTAMP,
        taken TIMESTAMP,
        FOREIGN KEY (slot_id) REFERENCES Slot(id)
    );