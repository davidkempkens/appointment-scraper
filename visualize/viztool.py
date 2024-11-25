from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import sqlite3
import repository.SlotRepository as repo


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

    city = city.lower()

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

    if exclude_office:
        df = df[df["office"] != exclude_office]

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


def count_per_timestamp(
    city: str,
    concern: str | None,
    office: str | None = None,
    exclude_office: str | None = None,
    from_csv: bool = False,
):

    return repo.SlotRepository(db=sqlite3.connect(f"db/{city}.db")).count_per_timestamp(
        city=city,
        concern=concern,
        office=office,
        exclude_office=exclude_office,
        from_csv=from_csv,
    )

    df = retrieveSlotData(city, concern, office, exclude_office)
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

    count_per_timestamp = pd.DataFrame({"timestamp": timestamps, "count": count})

    # save as csv
    count_per_timestamp.to_csv("count_per_timestamp.csv")

    return count_per_timestamp


def plot_count_per_timestamp(
    city: str,
    concern: str | None,
    office: str | None = None,
    exclude_office: str | None = None,
    from_csv: bool = False,
):
    count_df = count_per_timestamp(city, concern, office, exclude_office, from_csv)

    count_df.plot(
        x="timestamp",
        y="count",
        kind="line",
        figsize=(20, 10),
        # grid=True,
        title="Verfügbare Termine über die Zeit",
        xlabel="Zeit",
        ylabel="Anzahl verfügbarer Termine",
        legend=False,
    )

    # plot vertical line for each day at 7:00
    for i in range(1, 10):
        plt.axvline(
            x=count_df["timestamp"].iloc[0] + pd.Timedelta(days=i, hours=9),
            color="red",
            linestyle="--",
        )

    plt.show()


def calc_time_until_next_slots(
    city: str,
    concern: str | None,
    office: str | None = None,
    exclude_office: str | None = None,
):
    df = retrieveSlotData(city, concern, office, exclude_office)
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
    city: str,
    concern: str | None,
    office: str | None = None,
    window: str = "4h",
    exclude_office: str | None = None,
):
    time_until_slot = calc_time_until_next_slots(city, concern, office, exclude_office)

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


def group_by_slot_id(
    city: str,
    concern: str | None,
    office: str | None = None,
    exclude_office: str | None = None,
):
    df = retrieveSlotData(city, concern, office, exclude_office)
    slots = df.groupby("s_id")[
        [
            "office",
            "city",
            "concern",
            "hour",
            "weekday",
            "total_delta",
            "count_availabilities",
        ]
    ].first()
    return slots


def plot_mean_total_delta_per_weekday(
    city: str,
    concern: str | None,
    office: str | None = None,
    exclude_office: str | None = None,
):
    slots = group_by_slot_id(city, concern, office, exclude_office)
    mean_total_delta_per_weekday = slots.groupby("weekday")["total_delta"].mean()

    mean_total_delta_per_weekday = (
        mean_total_delta_per_weekday.dt.total_seconds() / 3600
    )

    # Definieren Sie die richtige Reihenfolge der Wochentage
    weekday_order = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]

    # Wochentage in der DataFrame zu deutschen Wochentagen umbenennen
    mean_total_delta_per_weekday.index = mean_total_delta_per_weekday.index.map(
        {
            "Monday": "Montag",
            "Tuesday": "Dienstag",
            "Wednesday": "Mittwoch",
            "Thursday": "Donnerstag",
            "Friday": "Freitag",
        }
    )

    # Stellen Sie sicher, dass die Wochentage in der richtigen Reihenfolge sind
    mean_total_delta_per_weekday = mean_total_delta_per_weekday.reindex(weekday_order)

    # Daten plotten
    mean_total_delta_per_weekday.plot(
        kind="bar",
        title="Durchschnittliche Zeit, die ein Termin 'buchbar' ist abhängig vom Wochentag, an dem der Termin stattfindet",
        ylabel="Stunden",
        xlabel="Wochentag",
        rot=45,
    )

    plt.show()


def plot_mean_total_delta_per_hour(
    city: str,
    concern: str | None,
    office: str | None = None,
    exclude_office: str | None = None,
):
    slots = group_by_slot_id(city, concern, office, exclude_office)
    mean_total_delta_per_hour = slots.groupby("hour")["total_delta"].mean()
    mean_total_delta_per_hour = mean_total_delta_per_hour.dt.total_seconds() / 3600

    # Daten plotten
    mean_total_delta_per_hour.plot(
        kind="bar",
        title="Durchschnittliche Zeit, die ein Termin 'buchbar' ist abhängig von der Stunde, zu der der Termin stattfindet",
        ylabel="Stunden",
        xlabel="Stunde",
        rot=0,
    )

    plt.show()
