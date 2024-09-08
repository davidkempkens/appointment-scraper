import sys
from cities.bremen import bremen
from cities.dresden import dresden
from cities.duesseldorf import duesseldorf
from cities.hannover import hannover
from cities.kiel import kiel
from cities.magdeburg import magdeburg
from cities.mainz import mainz
from cities.wiesbaden import wiesbaden
from datetime import datetime


def main():

    try:
        if len(sys.argv) > 1:
            city = sys.argv[1].lower()
            {
                "bremen": bremen,
                "dresden": dresden,
                "duesseldorf": duesseldorf,
                "hannover": hannover,
                "kiel": kiel,
                "magdeburg": magdeburg,
                "mainz": mainz,
                "wiesbaden": wiesbaden,
            }.get(city, lambda: print("City not found"))()

    except Exception as e:
        print(f"An error occured: {e} at: {datetime.now()}")

        # try again
        print("Trying again...")
        # main()


if __name__ == "__main__":
    main()
