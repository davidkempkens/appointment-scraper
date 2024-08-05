CREATE TABLE
    IF NOT EXISTS Stadt (name VARCHAR(255) PRIMARY KEY NOT NULL);

CREATE TABLE
    IF NOT EXISTS BuergerBuero (
        stadtteil VARCHAR(255) PRIMARY KEY NOT NULL,
        stadt VARCHAR(255) NOT NULL,
        FOREIGN KEY (stadt) REFERENCES Stadt (name)
    );

CREATE TABLE
    IF NOT EXISTS Termin (
        buergerbuero VARCHAR(255) NOT NULL,
        datum DATE NOT NULL,
        angelegenheit VARCHAR(255),
        -- save timestamp when the appointment was first recorded 
        erstmalsErfasstAlsFrei TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        erstmalsErfasstAlsBelegt TIMESTAMP,
        PRIMARY KEY (datum, buergerbuero),
        FOREIGN KEY (buergerbuero) REFERENCES BuergerBuero (stadtteil)
    );