from scraper.browser import Browser
import slots.slots as slots
from slots.slots import Slot as Slot
import db.database as db


HANNOVER = {
    "base_url": "http://termin.hannover-stadt.de/buergeramt",
    "plz": "30159",
    "offices": {
        "Aegi": "Aegi",
        "Bemerode": "Bemerode",
        "Doehren": "Doehren",
        "Herrenhausen": "Herrenhausen",
        "Linden": "Linden",
        "Podbi-Park": "Podbi-Park",
        "Ricklingen": "Ricklingen",
        "Sahlkamp": "Sahlkamp",
        "Schuetzenplatz": "Schuetzenplatz",
    },
    "concerns": {
        "personalausweis_antrag": {
            "id": "service_ede3dafc-4941-4e08-9526-bd70d77160ce",
            "name": "Personalausweis - Antrag",
        },
    },
}


def hannover():
    hannover = get_open_slots_from_hannover(concern="personalausweis_antrag")

    db.save_slots_per_city(hannover, "Hannover")


def get_open_slots_from_hannover(concern) -> list[Slot]:
    all_open_slots = []

    with Browser() as browser:
        browser.land_first_page(url=HANNOVER["base_url"])

        # enter postal code because it is prompted
        browser.get_element_with_id("input-field").send_keys(HANNOVER["plz"])

        # select Personalausweis
        select_element = browser.get_element_with_id(
            HANNOVER["concerns"][concern]["id"]
        )
        browser.select_option_by_value(select_element, "1")
        browser.get_element_with_attribute("data-testid", "button_next").click()

        browser.click_button_with_id("locations_selected_all_top")
        browser.click_button_with_id("next-button")

        slots_element = browser.get_elements_with_class("timeslot_cards")
        all_open_slots = browser.get_open_slots_from_element(slots_element)

        browser.quit()

    return slots.add_concern_to_slots(all_open_slots, "Personalausweis - Antrag")
