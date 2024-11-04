from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import sqlite3


def fetch_slots_from_db(city: str, concern: str | None):

    conn = sqlite3.connect(f"db/{city.lower()}.db")

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
    JOIN Availabilities ON Slots.id = Availabilities.slot_id
    WHERE concern = ?;
    """

    df = pd.read_sql_query(
        sql, conn, parse_dates=["available", "taken", "timeslot"], params=(concern,)
    )

    conn.close()

    # if concern:
    #     df = df[df["concern"] == concern]

    return df


def get_open_slots(city: str, concern: str | None = "Personalausweis - Antrag"):
    df = fetch_slots_from_db(city=city, concern=concern)

    df["offen"] = df["taken"].isnull()
    slots = df.groupby("office").offen.sum().sort_values(ascending=False)
    return slots


@callback(
    Output(component_id="controls-and-line-graph", component_property="figure"),
    Input(component_id="controls-and-radio-item", component_property="value"),
)
def count_open_slots_over_time(city):
    df = fetch_slots_from_db(city=city, concern="Personalausweis - Antrag")

    timestamps = pd.concat([df["available"], df["taken"]]).sort_values().unique()

    count = []
    for timestamp in timestamps:

        count_per_timestamp = df[
            (df["available"] <= timestamp)
            & ((df["taken"] >= timestamp) | (df["taken"].isnull()))
        ].shape[0]

        count.append(count_per_timestamp)

    open = pd.DataFrame({"Zeit": timestamps, "Termine": count})
    # print(open)

    return px.line(open, x="Zeit", y="Termine")


app = Dash()

app.layout = [
    html.Div(children="My Dash App"),
    dcc.RadioItems(
        options=[
            "Duesseldorf",
            "Dresden",
            "Bremen",
            "Hannover",
            "Kiel",
            "Mainz",
            "Wiesbaden",
        ],
        value="Duesseldorf",
        id="controls-and-radio-item",
    ),
    dcc.Graph(figure={}, id="controls-and-line-graph"),
    dcc.Graph(figure={}, id="controls-and-graph"),
    dash_table.DataTable(
        id="table",
        data=get_open_slots("Duesseldorf").reset_index().to_dict("records"),
    ),
]


@callback(
    Output(component_id="table", component_property="data"),
    Input(component_id="controls-and-radio-item", component_property="value"),
)
def update_table(city):
    open_appointments = get_open_slots(city)
    return open_appointments.reset_index().to_dict("records")


@callback(
    Output(component_id="controls-and-graph", component_property="figure"),
    Input(component_id="controls-and-radio-item", component_property="value"),
)
def update_graph(city):
    return px.bar(
        get_open_slots(city).reset_index(),
        x="office",
        y="offen",
        title=f"Offene Termine in {city}",
        labels={"offen": "Anzahl offener Termine", "office": "Bürgerbüro"},
        text_auto=True,
        # color="buergerbuero",
    )


if __name__ == "__main__":
    app.run(debug=True)
