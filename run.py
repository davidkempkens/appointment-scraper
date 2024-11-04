import sys
from cities.bremen import bremen
from cities.dresden import dresden
from cities.duesseldorf import duesseldorf
from cities.duesseldorf import debug
from cities.duesseldorf import init
from cities.hannover import hannover
from cities.kiel import kiel
from cities.magdeburg import magdeburg
from cities.mainz import mainz
from cities.wiesbaden import wiesbaden
from cities.wuppertal import wuppertal
from datetime import datetime


CONCERNS = {
    "anmeldung": "Anmeldung",
    "ummeldung": "Ummeldung",
    "abmeldung": "Abmeldung",
    "personalausweis_antrag": "Personalausweis - Antrag",
    "reisepass_antrag": "Reisepass - Antrag",
    "meldebescheinigung": "Meldebescheinigung",
}

CITIES = [
    "bremen",
    "dresden",
    "duesseldorf",
    "hannover",
    "kiel",
    "magdeburg",
    "mainz",
    "wiesbaden",
    "wuppertal",
]

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


def main():

    try:

        if len(sys.argv) == 2 and sys.argv[1] == "init":
            init(cities=CITIES)
            return
        if len(sys.argv) != 3:
            print("Usage: python run.py <city> <concern>")
            print()

            print("Example: python run.py bremen anmeldung")
            print()

            print("Available cities:")
            for city in CITIES:
                print(city)

            print()
            print("Available concerns:")
            for concern in CONCERNS:
                print(concern)
            return

        city = sys.argv[1].lower()

        if city not in CITIES:
            print(f"City not found: {city}")
            return

        concern = sys.argv[2].lower()

        if concern not in CONCERNS:
            print(f"Concern not found: {concern}")
            return

        # print(f"Running {city} for {concern} at: {datetime.now()}")
        if city == "bremen":
            bremen(concern)
        elif city == "dresden":
            dresden(concern)
        elif city == "duesseldorf":
            duesseldorf(concern)
        elif city == "hannover":
            hannover(concern)
        elif city == "kiel":
            kiel(concern)
        elif city == "magdeburg":
            magdeburg(concern)
        elif city == "mainz":
            mainz(concern)
        elif city == "wiesbaden":
            wiesbaden(concern)
        elif city == "wuppertal":
            wuppertal(concern)
        else:
            print(f"City not found: {city}")

    except Exception as e:

        print(
            f'{colors["fail"]}{datetime.now().strftime("%H:%M")} Error {e}{colors["end"]}'
        )
        raise e

    # try again
    # print("Trying again...")
    # main()


if __name__ == "__main__":
    main()
