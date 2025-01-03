import sqlite3
from bs4 import BeautifulSoup
from repository.SlotRepository import SlotRepository
from scraper.browser import Browser
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
        "reisepass_antrag": {
            "id": "button-plus-563",
            "name": "Reisepass - Antrag",
        },
        "anmeldung": {
            "id": "button-plus-577",
            "name": "Anmeldung",
        },
        "ummeldung": {
            "id": "button-plus-591",
            "name": "Ummeldung",
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


def kiel(concern: str = "personalausweis_antrag"):

    # slot_repository = SlotRepository(db=sqlite3.connect("db/kiel.db")).reset_db()
    # return

    online_slots = get_open_slots_from_kiel(concern)

    concern_name = KIEL["concerns"][concern]["name"]

    slot_repository = SlotRepository(db=sqlite3.connect("db/kiel.db"))
    report = slot_repository.synchronize_slots(
        online_slots, city="Kiel", concern=concern_name
    )

    slot_repository.print(report, city="Kiel", concern=concern_name)


def get_open_slots_from_kiel(concern):
    all_open_slots = []

    try:
        with Browser() as browser:
            browser.land_first_page(url=KIEL["base_url"])

            browser.click_button_with_id("cookie_msg_btn_no")  # Decline Cookies

            concern = KIEL["concerns"][concern]
            browser.click_button_with_id(concern["id"])

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
                all_open_slots.extend(
                    browser.get_open_slots_for_one_office(
                        tab, city="Kiel", concern=concern["name"]
                    )
                )
                # browser.close()
    finally:
        browser.quit()

    return all_open_slots
