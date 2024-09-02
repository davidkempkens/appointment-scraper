import sys
from cities.bremen import bremen
from cities.dresden import dresden
from cities.duesseldorf import duesseldorf
from cities.hannover import hannover
from cities.wiesbaden import wiesbaden


def main():

    try:
        if len(sys.argv) > 1:
            city = sys.argv[1].lower()
            if city == "duesseldorf":
                duesseldorf()
            elif city == "dresden":
                dresden()
            elif city == "bremen":
                bremen()
            elif city == "hannover":
                hannover()
            elif city == "wiesbaden":
                wiesbaden()
            else:
                print("City not found")

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
