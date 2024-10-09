from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import sqlite3


def fetch_slots_from_db():
    db_file = "db/database.db"
    conn = sqlite3.connect(db_file)

    sql = """
    SELECT *
    FROM Termin
    INNER JOIN BuergerBuero ON Termin.buergerbuero = BuergerBuero.stadtteil;"""

    df = pd.read_sql_query(
        sql,
        conn,
        parse_dates=["datum", "erstmalsErfasstAlsFrei", "erstmalsErfasstAlsBelegt"],
    )
    conn.close()
    return df


def get_open_slots(city):
    df = fetch_slots_from_db()

    df["offen"] = df["erstmalsErfasstAlsBelegt"].isnull()
    slots = (
        df[df["stadt"] == city]
        .groupby("buergerbuero")
        .offen.sum()
        .sort_values(ascending=False)
    )
    return slots


@callback(
    Output(component_id="controls-and-line-graph", component_property="figure"),
    Input(component_id="controls-and-radio-item", component_property="value"),
)
def count_open_slots_over_time(city):
    df = fetch_slots_from_db()

    # alle Termine in Düsseldorf
    df_city = df[df["stadt"] == city]

    # sortiere aufsteigend nach belegt-Zeitpunkt
    timestamps = df_city["erstmalsErfasstAlsBelegt"].sort_values().unique()

    count_open_per_timestamp = []

    for timestamp in timestamps:

        # pro Zeitpunkt: wie viele Termine sind offen?
        # Termine sind zu einem Zeitpunkt offen, wenn ...
        count = df_city[
            # der Anlegezeitpunkt vor (oder auf) dem Zeitpunkt liegt
            (df_city["erstmalsErfasstAlsFrei"] <= timestamp)
            # und ...
            & (
                # der Belegtzeitpunkt entweder nach dem Zeitpunkt liegt
                (timestamp < df_city["erstmalsErfasstAlsBelegt"])
                # oder gar nicht gesetzt ist
                | (df_city["erstmalsErfasstAlsBelegt"].isnull())
            )
        ].shape[0]
        count_open_per_timestamp.append(count)

    open = pd.DataFrame({"Zeit": timestamps, "Termine": count_open_per_timestamp})

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
        x="buergerbuero",
        y="offen",
        title=f"Offene Termine in {city}",
        labels={"offen": "Anzahl offener Termine", "buergerbuero": "Bürgerbüro"},
        text_auto=True,
        # color="buergerbuero",
    )


if __name__ == "__main__":
    app.run(debug=True)
