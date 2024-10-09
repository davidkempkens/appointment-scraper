from datetime import datetime
import locale

OFFICES = {
    "Bremen": [
        {
            "name": "BürgerServiceCenter-Mitte",
            "pk_sql": "BuergerServiceCenter-Mitte",
            "currently": "BuergerServiceCenter-Mitte",
        }
    ],
    "Dresden": [
        {"name": "Bürgerbüro Altstadt", "pk_sql": "Buergerbuero_Altstadt"},
        {"name": "Bürgerbüro Blasewitz", "pk_sql": "Buergerbuero_Blasewitz"},
        {"name": "Meldestelle Cossebaude", "pk_sql": "Meldestelle_Cossebaude"},
        {"name": "Bürgerbüro Cotta", "pk_sql": "Buergerbuero_Cotta"},
        {"name": "Junioramt", "pk_sql": "Junioramt"},
        {"name": "Bürgerbüro Klotzsche", "pk_sql": "Buergerbuero_Klotzsche"},
        {"name": "Meldestelle Langebrück", "pk_sql": "Meldestelle_Langebrueck"},
        {"name": "Bürgerbüro Leuben", "pk_sql": "Buergerbuero_Leuben"},
        {"name": "Bürgerbüro Neustadt", "pk_sql": "Buergerbuero_Neustadt"},
        {"name": "Bürgerbüro Pieschen", "pk_sql": "Buergerbuero_Pieschen"},
        {"name": "Bürgerbüro Plauen", "pk_sql": "Buergerbuero_Plauen"},
        {"name": "Bürgerbüro Prohlis", "pk_sql": "Buergerbuero_Prohlis"},
        {"name": "Meldestelle Weixdorf", "pk_sql": "Meldestelle_Weixdorf"},
    ],
    "Duesseldorf": [
        {"name": "Bürgerbüro Benrath", "pk_sql": "Buergerbuero_Benrath"},
        {"name": "Bürgerbüro Bilk", "pk_sql": "Buergerbuero_Bilk"},
        {
            "name": "Bürgerbüro Dienstleistungszentrum",
            "pk_sql": "Buergerbuero_Dienstleistungszentrum",
        },
        {"name": "Bürgerbüro Eller", "pk_sql": "Buergerbuero_Eller"},
        {"name": "Bürgerbüro Garath", "pk_sql": "Buergerbuero_Garath"},
        {"name": "Bürgerbüro Gerresheim", "pk_sql": "Buergerbuero_Gerresheim"},
        {"name": "Bürgerbüro Kaiserswerth", "pk_sql": "Buergerbuero_Kaiserswerth"},
        {"name": "Bürgerbüro Oberkassel", "pk_sql": "Buergerbuero_Oberkassel"},
        {"name": "Bürgerbüro Rath", "pk_sql": "Buergerbuero_Rath"},
        {"name": "Bürgerbüro Unterbach", "pk_sql": "Buergerbuero_Unterbach"},
        {
            "name": "Bürgerbüro Wersten/Holthausen",
            "pk_sql": "Buergerbuero_Wersten_Holthausen",
        },
    ],
    "Hannover": [
        {"name": "Bürgeramt Aegi", "pk_sql": "Buergeramt_Aegi"},
        {"name": "Bürgeramt Bemerode", "pk_sql": "Buergeramt_Bemerode"},
        {"name": "Bürgeramt Doehren", "pk_sql": "Buergeramt_Doehren"},
        {"name": "Bürgeramt Herrenhausen", "pk_sql": "Buergeramt_Herrenhausen"},
        {"name": "Bürgeramt Linden", "pk_sql": "Buergeramt_Linden"},
        {"name": "Bürgeramt Podbi-Park", "pk_sql": "Buergeramt_Podbi_Park"},
        {"name": "Bürgeramt Ricklingen", "pk_sql": "Buergeramt_Ricklingen"},
        {"name": "Bürgeramt Sahlkamp", "pk_sql": "Buergeramt_Sahlkamp"},
        {"name": "Bürgeramt Schuetzenplatz", "pk_sql": "Buergeramt_Schuetzenplatz"},
    ],
    "Kiel": [
        {"name": "Dietrichsdorf Stadtteilamt", "pk_sql": "Dietrichsdorf_Stadtteilamt"},
        {"name": "Elmschenhagen Stadtteilamt", "pk_sql": "Elmschenhagen_Stadtteilamt"},
        {"name": "Hassee Stadtteilamt", "pk_sql": "Hassee_Stadtteilamt"},
        {"name": "Mettenhof Stadtteilamt", "pk_sql": "Mettenhof_Stadtteilamt"},
        {"name": "Pries Stadtteilamt", "pk_sql": "Pries_Stadtteilamt"},
        {"name": "Rathaus", "pk_sql": "Rathaus"},
        {"name": "Suchsdorf Stadtteilamt", "pk_sql": "Suchsdorf_Stadtteilamt"},
    ],
    "Magdeburg": [
        {"name": "BürgerBüro Mitte", "pk_sql": "BuergerBuero_Mitte"},
        {"name": "BürgerBüro Nord", "pk_sql": "BuergerBuero_Nord"},
        {"name": "BürgerBüro Süd", "pk_sql": "BuergerBuero_Sued"},
        {"name": "BürgerBüro West", "pk_sql": "BuergerBuero_West"},
    ],
    "Mainz": [
        {"name": "Ortsverwaltung Marienborn", "pk_sql": "Ortsverwaltung_Marienborn"},
        {"name": "Ortsverwaltung Finthen", "pk_sql": "Ortsverwaltung_Finthen"},
        {"name": "Ortsverwaltung Hechtsheim", "pk_sql": "Ortsverwaltung_Hechtsheim"},
        {"name": "Ortsverwaltung Weisenau", "pk_sql": "Ortsverwaltung_Weisenau"},
        {"name": "Ortsverwaltung Ebersheim", "pk_sql": "Ortsverwaltung_Ebersheim"},
        {"name": "Ortsverwaltung Drais", "pk_sql": "Ortsverwaltung_Drais"},
        {"name": "Bürgerservice Stadthaus", "pk_sql": "Buergerservice_Stadthaus"},
        {"name": "Ortsverwaltung Lerchenberg", "pk_sql": "Ortsverwaltung_Lerchenberg"},
        {"name": "Ortsverwaltung Gonsenheim", "pk_sql": "Ortsverwaltung_Gonsenheim"},
        {
            "name": "Ortsverwaltung Hartenberg-Münchfeld",
            "pk_sql": "Ortsverwaltung_Hartenberg_Muenchfeld",
        },
        {"name": "Ortsverwaltung Altstadt", "pk_sql": "Ortsverwaltung_Altstadt"},
        {"name": "Ortsverwaltung Laubenheim", "pk_sql": "Ortsverwaltung_Laubenheim"},
        {"name": "Ortsverwaltung Mombach", "pk_sql": "Ortsverwaltung_Mombach"},
        {"name": "Ortsverwaltung Bretzenheim", "pk_sql": "Ortsverwaltung_Bretzenheim"},
        {"name": "Ortsverwaltung Oberstadt", "pk_sql": "Ortsverwaltung_Oberstadt"},
        {"name": "Ortsverwaltung Neustadt", "pk_sql": "Ortsverwaltung_Neustadt"},
    ],
    "Wiesbaden": [
        {"name": "Bürgerbüro Marktstraße", "pk_sql": "Buergerbuero_Marktstrasse"},
    ],
}


def convert_to_datetime(date):
    if date is None:
        return None
    if isinstance(date, datetime):
        return date
    return datetime.fromisoformat(date)


class Slot:
    """
    A slot is a date and time at a specific office

    office: str - the name of the office
    date: datetime - the date of the slot
    created: datetime - the date the slot was created
    updated: datetime - the date the slot was not available for the first time
    """

    def __init__(
        self,
        office: str,
        date: datetime | str,
        concern: str | None = None,
        created: datetime | str = datetime.now(),
        updated: datetime | str | None = None,
    ):
        """
        office: str - the name of the office
        date: datetime | str - the date of the slot
        created: datetime | str - the date the slot was available for the first time
        updated: datetime | str - the date the slot was not available for the first time
        """
        self.office = convert_german_vowels(office)
        self.date = convert_to_datetime(date)
        self.concern = concern
        self.created: datetime | str = convert_to_datetime(created)
        self.updated: datetime | str = convert_to_datetime(updated)

    def __eq__(self, other):
        return str(self.office) == str(other.office) and str(self.date) == str(
            other.date
        )

    def __repr__(self):
        return f"{self.office}: {self.date.strftime('%a %d.%m %H:%M')} - {self.concern}"
        # return f"Slot({self.office}, {self.date})"


def create_slots(slots: list[tuple]) -> list[Slot]:
    """
    creates a list of slots from a list of tuples

    slots: list[tuple] - a list of tuples with the format (office, date[, concern [, created [, updated]]])
    """
    if isinstance(slots, tuple):
        slots = [slots]

    return [Slot(*slot) for slot in slots if not isinstance(slot, Slot)]


def difference(A: list[Slot], B: list[Slot]) -> list[Slot]:
    """
    returns all slots in A that are not in B
    """
    return [a for a in A if a not in B]


def new_difference(A: list[Slot], B: list[Slot]) -> list[Slot]:
    """
    returns all slots in A that are not in B
    """
    not_in_b = []

    # print("len(A):", len(A))
    # print("len(B):", len(B))
    for a in A:
        a_found_in_b = False
        for b in B:
            if a == b:
                a_found_in_b = True
                # print(f"{a} == {b}")
                break
            # else:
            # print(f"{a} != {b}")
        if not a_found_in_b:
            print(f"{a} not in B")
            not_in_b.append(a)
    return not_in_b


def add_concern_to_slots(slots: list[Slot], concern: str) -> list[Slot]:
    """
    adds a concern to all slots
    """
    for slot in slots:
        slot.concern = concern
    return slots


def convert_german_vowels(string):
    return string.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue")


def print_slots(slots, text="", color=None):

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

    # set locale to german
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")

    print(f"{colors[color]}{text}")

    for slot in slots:
        print(slot)
    print(f"{colors['end']}")
