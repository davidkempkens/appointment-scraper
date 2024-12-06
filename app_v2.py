from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import sqlite3
import repository.SlotRepository as repository
from visualize import viztool


def fetch_slots_from_db(
    city: str,
    concern: str | None,
    office: str | None = None,
    exclude_office: str | None = None,
):
    df = viztool.read_data_from_csv()

    if city:
        df = df[df["city"] == city]
    if concern:
        df = df[df["concern"] == concern]
    if office:
        df = df[df["office"] == office]
    if exclude_office:
        df = df[df["office"] != exclude_office]

    return df


def get_open_slots(city: str, concern: str | None = "Personalausweis - Antrag"):
    df = fetch_slots_from_db(city=city, concern=concern)

    df["offen"] = df["taken"].isnull()
    slots = df.groupby("office").offen.sum().sort_values(ascending=False)
    return slots


@callback(
    Output(component_id="controls-and-line-graph", component_property="figure"),
    Input(component_id="controls-and-radio-item", component_property="value"),
    Input(component_id="controls-and-radio-concern", component_property="value"),
    Input(component_id="controls-and-radio-office", component_property="value"),
)
def count_open_slots_over_time(city, concern="Personalausweis - Antrag", office=None):
    print(
        concern,
        city,
        office,
        "Fetching from db at",
        pd.Timestamp.now().strftime("%H:%M"),
    )

    open = viztool.create_time_series(
        df=viztool.read_data_from_csv(),
        city=city,
        concern=concern,
        office=office,
        exclude_office=None,
    )

    first_timestamp = open["timestamp"].min().strftime("%d.%m.")
    last_timestamp = open["timestamp"].max().strftime("%d.%m. %H:%M")

    return px.line(
        open,
        x="timestamp",
        y="count",
        title=f"{concern} in {city} {office if office else ''}",
        labels={
            "count": "Anzahl offener Termine",
            "timestamp": f"Zeitraum vom {first_timestamp} bis zum {last_timestamp}",
        },
    )


@callback(
    Output(component_id="controls-and-graph", component_property="figure"),
    Input(component_id="controls-and-radio-item", component_property="value"),
    Input(component_id="controls-and-radio-concern", component_property="value"),
)
def update_graph(city, concern):

    open = get_open_slots(city, concern)
    count = open.sum()
    return px.bar(
        open.reset_index(),
        x="office",
        y="offen",
        title=f"{concern} in {city}: {count} um {pd.Timestamp.now().strftime('%H:%M Uhr')}",
        labels={"offen": "Anzahl offener Termine", "office": "Bürgerbüro"},
        text_auto=True,
        # color="buergerbuero",
    )


@callback(
    Output(component_id="controls-and-radio-office", component_property="options"),
    Input(component_id="controls-and-radio-item", component_property="value"),
    Input(component_id="controls-and-radio-concern", component_property="value"),
)
def update_radio_office(city, concern):
    offices = fetch_slots_from_db(city=city, concern=concern)["office"].unique()

    return [{"label": office, "value": office} for office in offices].append(
        {"label": "Alle", "value": None}
    )


app = Dash()

app.layout = html.Div(
    [
        html.Div(
            dcc.Graph(figure={}, id="controls-and-line-graph"),
            className="time-graph",
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.RadioItems(
                            options=[
                                "Duesseldorf",
                                "Dresden",
                                "Kiel",
                            ],
                            value="Duesseldorf",
                            id="controls-and-radio-item",
                        ),
                        dcc.RadioItems(
                            options=[
                                "Personalausweis - Antrag",
                                "Reisepass - Antrag",
                                "Anmeldung",
                                "Ummeldung",
                                "Abmeldung",
                            ],
                            value="Personalausweis - Antrag",
                            id="controls-and-radio-concern",
                        ),
                        dcc.RadioItems(
                            id="controls-and-radio-office",
                            # options=[],
                            # value="",
                        ),
                    ],
                    className="controls",
                ),
                html.Div(
                    dcc.Graph(figure={}, id="controls-and-graph"),
                    className="count-graph",
                ),
            ],
            className="wrapper",
        ),
    ],
    className="container",
)


if __name__ == "__main__":
    app.run(debug=True)
