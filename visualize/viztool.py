from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import sqlite3


def retrieveSlotData(city: str, concern: str | None, office: str | None = None):

    conn = sqlite3.connect(f"db/{city}.db")

    sql = """
    SELECT 
        Availabilities.slot_id as s_id,
        Slots.office as office,
        Slots.city as city,
        Slots.timeslot as timeslot,
        Slots.concern as concern,
        Availabilities.id as a_id,
        Availabilities.available as available,
        Availabilities.taken as taken
    FROM Slots
    JOIN Availabilities ON Slots.id = Availabilities.slot_id;
    """

    df = pd.read_sql_query(sql, conn, parse_dates=["available", "taken", "timeslot"])

    conn.close()

    if concern:
        df = df[df["concern"] == concern]

    if office:
        df = df[df["office"] == office]

    return preprocess_dataframe(df)


def preprocess_dataframe(df):

    # add count of availabilities per s_id
    df["count_availabilities"] = df.groupby("s_id")["a_id"].transform("count")

    # lose precision to only minutes
    df["timeslot"] = df["timeslot"].dt.floor("min")
    df["available"] = df["available"].dt.floor("min")
    df["taken"] = df["taken"].dt.floor("min")

    # add weekday
    df["weekday"] = df["timeslot"].dt.day_name()

    # add hour
    df["hour"] = df["timeslot"].dt.hour

    # timedelta between available and taken
    df["delta"] = df["taken"] - df["available"]

    # time until slot
    df["time_until_slot"] = df["timeslot"] - df["taken"]

    # add total delta per s_id
    df["total_delta"] = df.groupby("s_id")["delta"].transform("sum")

    # sort by total delta
    df = df.sort_values("s_id", ascending=True)

    return df


def count_per_timestamp(city: str, concern: str | None, office: str | None = None):
    df = retrieveSlotData(city, concern, office)
    # get all unique timestamps from available and taken
    timestamps = pd.concat([df["available"], df["taken"]]).sort_values().unique()
    count = pd.Series(dtype=int)
    for timestamp in timestamps:
        # count slots for each timestamp
        count_per_timestamp = df[
            (df["available"] <= timestamp)
            & ((df["taken"] >= timestamp) | (df["taken"].isnull()))
        ].shape[0]
        count.at[timestamp] = count_per_timestamp
    return pd.DataFrame({"timestamp": timestamps, "count": count})


def plot_count_per_timestamp(city: str, concern: str | None, office: str | None = None):
    count_df = count_per_timestamp(city, concern, office)

    count_df.plot(
        x="timestamp",
        y="count",
        kind="line",
        figsize=(20, 10),
        grid=True,
        title="Verfügbare Termine über die Zeit",
        xlabel="Zeit",
        ylabel="Anzahl verfügbarer Termine",
        legend=False,
    )


def calc_time_until_next_slots(
    city: str, concern: str | None, office: str | None = None
):
    df = retrieveSlotData(city, concern, office)
    # print(df.shape)
    # return df
    time_until_slot = df.groupby(by="available").agg(
        {"timeslot": ["min", "max", "mean"]}
    )

    conversion_factor = 1 / (3600 * 24)
    # return time_until_slot

    time_until_slot["time_until_slot_mean"] = (
        time_until_slot["timeslot"]["mean"] - time_until_slot.index
    ).dt.total_seconds() * conversion_factor

    time_until_slot["time_until_slot_min"] = (
        time_until_slot["timeslot"]["min"] - time_until_slot.index
    ).dt.total_seconds() * conversion_factor

    time_until_slot["time_until_slot_max"] = (
        time_until_slot["timeslot"]["max"] - time_until_slot.index
    ).dt.total_seconds() * conversion_factor

    return time_until_slot


def plot_time_until_next_slots(
    city: str, concern: str | None, office: str | None = None, window: str = "4h"
):
    time_until_slot = calc_time_until_next_slots(city, concern, office)

    time_until_slot = time_until_slot.resample("min").ffill()

    fig, ax = plt.subplots(figsize=(20, 10))

    # ax.plot(
    #     time_until_slot.index,
    #     time_until_slot["time_until_slot_min"],
    #     label="Durchschnittliche Zeit bis zum Termin",
    # )

    time_until_slot["time_until_slot_min"].rolling(window).mean().plot(
        ax=ax,
        label=f"Gleitener Mittelwert der Breite {window}",
        grid=True,
    )

    # plot difference between min and max
    # ax.fill_between(
    #     time_until_slot.index,
    #     time_until_slot["time_until_slot_min"],
    #     time_until_slot["time_until_slot_max"],
    #     alpha=0.3,
    #     label="Difference between min and max",
    # )

    ax.xaxis.set_major_locator(mdates.HourLocator(interval=24))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%a %d.%m."))

    ax.set_title(
        "Gleitender Mittelwert der kürzesten Zeit bis zum nächsten Termin in Tagen"
    )
    ax.set_xlabel("Zeitpunkt der Abfrage")
    ax.set_ylabel("Zeit bis zum nächsten Termin in Tagen")
    ax.legend()

    plt.show()
