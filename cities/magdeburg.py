import sqlite3
from repository.SlotRepository import SlotRepository
from scraper.browser import Browser
import slots.slots as slots
from slots.slots import Slot as Slot
import db.database as db
from datetime import datetime

MAGDEBURG = {
    "base_url": "https://terminvergabe.magdeburg.de/select2?md=2",
    "area": {
        "personaldokumente": {
            "id": "header_concerns_accordion-22313",
            "name": "Personaldokumente",
        },
        "meldeangelegenheiten": {
            "id": "header_concerns_accordion-22309",
            "name": "Meldeangelegenheiten",
        },
    },
    "concerns": {
        "personalausweis_antrag": {
            "id": "button-plus-1984",
            "name": "Personalausweis - Antrag",
        },
        "reisepass_antrag": {
            "id": "button-plus-1994",
            "name": "Reisepass - Antrag",
        },
        "anmeldung": {
            "id": "button-plus-1930",
            "name": "Anmeldung",
        },
        "ummeldung": {
            "id": "button-plus-1923",
            "name": "Ummeldung",
        },
        "abmeldung": {
            "id": "button-plus-1939",
            "name": "Abmeldung",
        },
    },
    "offices": {
        "Mitte": {
            "name": "BürgerBüro Mitte",
        },
        "Nord": {
            "name": "BürgerBüro Nord",
        },
        "Sued": {
            "name": "BürgerBüro Süd",
        },
        "West": {
            "name": "BürgerBüro West",
        },
    },
}


def magdeburg(concern):

    # SlotRepository(db=sqlite3.connect("db/magdeburg.db")).reset_db()
    # return

    online_slots = get_open_slots_from_magdeburg(concern)

    slot_repo = SlotRepository(db=sqlite3.connect("db/magdeburg.db"))

    report = slot_repo.synchronize_slots(
        online_slots=online_slots,
        city="Magdeburg",
        concern=MAGDEBURG["concerns"][concern]["name"],
    )

    slot_repo.print(
        report, city="Magdeburg", concern=MAGDEBURG["concerns"][concern]["name"]
    )


def get_open_slots_from_magdeburg(concern):

    all_open_slots = []

    try:

        with Browser() as browser:
            browser.land_first_page(MAGDEBURG["base_url"])

            browser.click_button_with_id("cookie_msg_btn_no")  # Decline Cookies

            if concern in ["personalausweis_antrag", "reisepass_antrag"]:
                browser.click_button_with_id(
                    MAGDEBURG["area"]["personaldokumente"]["id"]
                )
            else:
                browser.click_button_with_id(
                    MAGDEBURG["area"]["meldeangelegenheiten"]["id"]
                )

            browser.click_button_with_id(MAGDEBURG["concerns"][concern]["id"])

            browser.click_button_with_id("WeiterButton")  # Weiter
            browser.click_button_with_id("OKButton")  # OK

            office_elements = browser.get_h3_containing_office_names(
                search_term="BürgerBüro"
            )
            tabs = browser.open_offices_in_new_tabs(office_elements)

            all_open_slots = browser.get_open_slots_from_tabs_for_all_offices(
                tabs, city="Magdeburg", concern=MAGDEBURG["concerns"][concern]["name"]
            )
    finally:
        browser.quit()
        pass
    return all_open_slots
