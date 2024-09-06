from bs4 import BeautifulSoup
from scraper.browser import Browser
import slots.slots as slots
from slots.slots import Slot as Slot
import db.database as db
from datetime import datetime


KIEL = {
    "base_url": "https://terminvergabe.kiel.de/tevis-ema/select2?md=1",
    "form_data": {
        "nachname": "Mustermann",
        "vorname": "Max",
        "email": "max.mustermann@mail.de",
        "telefon": "01234567890",
    },
    "concerns": {
        "personalausweis_antrag": {
            "id": "button-plus-549",
            "name": "Personalausweis - Antrag",
        },
    },
    "offices": {
        "Dietrichsdorf": {
            "name": "Dietrichsdorf Stadtteilamt",
            "value": "Dietrichsdorf Stadtteilamt  auswählen",
        },
        "Elmschenhagen": {
            "name": "Elmschenhagen Stadtteilamt",
            "value": "Elmschenhagen Stadtteilamt  auswählen",
        },
        "Hassee": {
            "name": "Hassee Stadtteilamt",
            "value": "Hassee Stadtteilamt  auswählen",
        },
        "Mettenhof": {
            "name": "Mettenhof Stadtteilamt",
            "value": "Mettenhof Stadtteilamt  auswählen",
        },
        "Pries": {
            "name": "Pries Stadtteilamt",
            "value": "Pries Stadtteilamt  auswählen",
        },
        "Rathaus": {
            "name": "Rathaus",
            "value": "Rathaus auswählen",
        },
        "Suchsdorf": {
            "id": "ui-id-13",
            "name": "Suchsdorf Stadtteilamt",
            "value": "Suchsdorf Stadtteilamt  auswählen",
        },
    },
}


def kiel():
    kiel = get_open_slots_from_kiel()

    db.save_slots_per_city(kiel, "Kiel")


def get_open_slots_from_kiel() -> list[Slot]:
    all_open_slots = []

    with Browser() as browser:
        browser.land_first_page(url=KIEL["base_url"])

        browser.click_button_with_id("cookie_msg_btn_no")  # Decline Cookies

        concern = KIEL["concerns"]["personalausweis_antrag"]  # Personalausweis - Antrag
        browser.click_button_with_id(concern["id"])  # Personalausweis - Antrag

        browser.click_button_with_id("WeiterButton")  # Weiter
        browser.click_button_with_id("OKButton")  # OK

        open_tabs_offices = {}

        for tab in KIEL["offices"]:
            h3 = browser.get_h3_containing_office_names(
                search_term=KIEL["offices"][tab]["name"]
            )[0]

            if "Termine" in h3.get_attribute("title"):
                if "false" in h3.get_attribute("aria-expanded"):
                    browser.click_element(h3)

                input_element = browser.get_element_with_attribute(
                    "value", KIEL["offices"][tab]["value"]
                )

                tab_to_office = browser.open_element_in_new_tab(input_element)

                open_tabs_offices[tab] = tab_to_office

        for tab in open_tabs_offices:
            browser.switch_to.window(open_tabs_offices[tab])
            all_open_slots.extend(browser.get_open_slots_for_one_office(tab))
            # browser.close()

        browser.quit()

    return slots.add_concern_to_slots(all_open_slots, "Personalausweis - Antrag")
