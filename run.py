import sys
from cities.dresden import dresden
from cities.duesseldorf import duesseldorf
from cities.kiel import kiel
from datetime import datetime


CONCERNS = {
    "anmeldung": "Anmeldung",
    "ummeldung": "Ummeldung",
    "abmeldung": "Abmeldung",
    "personalausweis_antrag": "Personalausweis - Antrag",
    "reisepass_antrag": "Reisepass - Antrag",
}

CITIES = [
    "dresden",
    "duesseldorf",
    "kiel",
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
        if city == "dresden":
            dresden(concern)
        elif city == "duesseldorf":
            duesseldorf(concern)
        elif city == "kiel":
            kiel(concern)
        else:
            print(f"City not found: {city}")

    except Exception as e:

        print(
            f'{colors["fail"]}{datetime.now().strftime("%H:%M")} Error {type(e).__name__}{colors["end"]}'
        )
        # raise e


if __name__ == "__main__":
    main()
