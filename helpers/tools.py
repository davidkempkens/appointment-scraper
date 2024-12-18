import numpy as np
import pandas as pd
import sqlite3
import repository.SlotRepository as repo


def read_data_from_csv():
    data = pd.read_csv(
        "db/data.csv",
        parse_dates=["timeslot", "available", "taken"],
    )

    # parse "delta", "time_until_slot" and "total_delta" as timedelta
    data["delta"] = pd.to_timedelta(data["delta"])
    data["time_until_slot"] = pd.to_timedelta(data["time_until_slot"])
    data["total_delta"] = pd.to_timedelta(data["total_delta"])

    return data


def create_time_series(
    df: pd.DataFrame,
    city: str = None,
    office: str = None,
    concern: str = None,
    exclude_office: str = None,
):

    if city is not None:
        if isinstance(city, str):
            city = city.capitalize()
            city = [city]
        df = df[df["city"].isin(city)]

    if office is not None:
        if isinstance(office, str):
            office = [office]
        df = df[df["office"].isin(office)]

    if exclude_office is not None:
        if isinstance(exclude_office, str):
            exclude_office = [exclude_office]
        df = df[~df["office"].isin(exclude_office)]

    if concern is not None:
        if isinstance(concern, str):
            concern = [concern]
        df = df[df["concern"].isin(concern)]

    timestamps = pd.concat([df["available"], df["taken"]]).sort_values().unique()
    count = pd.Series(dtype=int)

    available = df["available"].values
    taken = df["taken"].values

    count = np.array(
        [
            ((available <= timestamp) & ((taken >= timestamp) | pd.isnull(taken))).sum()
            for timestamp in timestamps
        ]
    )

    count_per_timestamp = pd.DataFrame({"timestamp": timestamps, "count": count})

    return count_per_timestamp


def retrieveSlotData(
    city: str,
    concern: str | None,
    office: str | None = None,
    exclude_office: str | None = None,
):

    slot_repo = repo.SlotRepository(db=sqlite3.connect(f"db/{city}.db"))
    return slot_repo.get_all(
        city=city, concern=concern, office=office, exclude_office=exclude_office
    )
