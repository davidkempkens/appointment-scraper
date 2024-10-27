from datetime import datetime


def convert_to_datetime(date):
    if date is None:
        return None
    if isinstance(date, datetime):
        return date
    return datetime.fromisoformat(date)


class Slot:

    def __init__(
        self,
        office: str,
        city: str,
        timeslot: datetime | str,
        concern: str,
    ):
        self.office = office
        self.city = city
        self.timeslot = convert_to_datetime(timeslot)
        self.concern = concern
        self.id = None

    def __eq__(self, other):
        if self.id is not None and other.id is not None:
            return self.id == other.id
        else:
            return (
                str(self.office) == str(other.office)
                and str(self.city) == str(other.city)
                and str(self.timeslot) == str(other.timeslot)
                and str(self.concern) == str(other.concern)
            )

    def __repr__(self):
        return f"{self.office}: {self.timeslot.strftime('%a %d.%m %H:%M')} - {self.concern}"

    @classmethod
    def make_from_db(cls, row):
        id = row[0]
        office = row[1]
        city = row[2]
        timeslot = row[3]
        concern = row[4]

        instance = cls(office, city, timeslot, concern)
        instance.id = id
        return instance

    def set_id(self, id):
        self.id = id
        return self
