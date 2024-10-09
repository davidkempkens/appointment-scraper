from datetime import datetime
import locale


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
