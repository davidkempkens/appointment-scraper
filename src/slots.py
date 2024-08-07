from datetime import datetime
import locale


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
        self.date = self.convert_to_datetime(date)
        self.concern = concern
        self.created: datetime | str = self.convert_to_datetime(created)
        self.updated: datetime | str = self.convert_to_datetime(updated)

    def convert_to_datetime(self, date):
        if date is None:
            return None
        if isinstance(date, datetime):
            return date
        return datetime.fromisoformat(date)

    def __eq__(self, other):
        return self.office == other.office and self.date == other.date

    def __hash__(self):
        return hash((self.office, self.date))

    def __repr__(self):
        return f"{self.office}: {self.date.strftime('%a %d.%m %H:%M')} - {self.concern}"
        # return f"Slot({self.office}, {self.date})"


def create_slots(slots: list[tuple]) -> list[Slot]:
    """
    creates a list of slots from a list of tuples

    slots: list[tuple] - a list of tuples with the format (office, date[, concern [, created [, updated]]])
    """
    return [Slot(*slot) for slot in slots if not isinstance(slot, Slot)]


def difference(A: list[Slot], B: list[Slot]) -> list[Slot]:
    """
    returns all slots in A that are not in B
    """
    return [a for a in A if a not in B]


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
