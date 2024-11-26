from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import sqlite3
import repository.SlotRepository as repository


def fetch_slots_from_db(
    city: str,
    concern: str | None,
    office: str | None = None,
    exclude_office: str | None = None,
):
    return repository.SlotRepository(
        db=sqlite3.connect(f"db/{city.lower()}.db")
    ).get_all(city=city, concern=concern, office=office, exclude_office=exclude_office)


def get_open_slots(city: str, concern: str | None = "Personalausweis - Antrag"):
    df = fetch_slots_from_db(city=city, concern=concern)

    df["offen"] = df["taken"].isnull()
    slots = df.groupby("office").offen.sum().sort_values(ascending=False)
    return slots


@callback(
    Output(component_id="controls-and-line-graph", component_property="figure"),
    Input(component_id="controls-and-radio-item", component_property="value"),
    Input(component_id="controls-and-radio-concern", component_property="value"),
)
def count_open_slots_over_time(city, concern="Personalausweis - Antrag"):
    open = repository.SlotRepository(
        db=sqlite3.connect(f"db/{city.lower()}.db")
    ).count_per_timestamp(
        city=city,
        concern=concern,
        from_csv=True,
    )

    first_timestamp = open["timestamp"].min().strftime("%d.%m.")
    last_timestamp = open["timestamp"].max().strftime("%d.%m. %H:%M")

    return px.line(
        open,
        x="timestamp",
        y="count",
        title=f"{concern} in {city}",
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
