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
    },
    "concerns": {
        "personalausweis": {
            "id": "button-plus-1984",
            "name": "Personalausweis - Antrag",
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


def magdeburg():
    magdeburg = get_open_slots_from_magdeburg()

    slots.print_slots(magdeburg)

    # print(len(magdeburg))

    # db.save_slots_per_city(magdeburg, "Magdeburg")


def get_open_slots_from_magdeburg():

    all_open_slots = []

    with Browser() as browser:
        browser.land_first_page(MAGDEBURG["base_url"])

        browser.click_button_with_id("cookie_msg_btn_no")  # Decline Cookies

        browser.click_button_with_id(MAGDEBURG["area"]["personaldokumente"]["id"])

        browser.click_button_with_id(MAGDEBURG["concerns"]["personalausweis"]["id"])

        browser.click_button_with_id("WeiterButton")  # Weiter
        browser.click_button_with_id("OKButton")  # OK

        office_elements = browser.get_h3_containing_office_names(
            search_term="BürgerBüro"
        )
        tabs = browser.open_offices_in_new_tabs(office_elements)

        all_open_slots = browser.get_open_slots_from_tabs_for_all_offices(tabs)

        browser.quit()
    return all_open_slots
