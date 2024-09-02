from scraper.browser import Browser
import slots.slots as slots
from slots.slots import Slot as Slot
import db.database as db

BREMEN = {
    "base_url": "https://termin.bremen.de/termine/select2?md=5",
    "einwohnerangelegenheiten": {
        "name": "Einwohnerangelegenheiten",
        "concerns": {
            "ausweise": {
                "id": "header_concerns_accordion-7738",
                "sub_concerns": {
                    "personalausweis_antrag": {
                        "id": "button-plus-9077",
                        "name": "Personalausweis - Antrag",
                    },
                },
            }
        },
    },
}


def bremen():
    bremen = get_open_slots_from_bremen(
        concern="ausweise", sub_concern="personalausweis_antrag"
    )

    db.save_slots_per_city(bremen, "Bremen")


def get_open_slots_from_bremen(concern, sub_concern) -> list[Slot]:
    all_open_slots = []

    try:
        with Browser() as browser:
            browser.land_first_page(url=BREMEN["base_url"])
            browser.click_button_with_id("cookie_msg_btn_no")  # Decline Cookies

            area = BREMEN["einwohnerangelegenheiten"]
            concern = area["concerns"][concern]
            sub_concern = concern["sub_concerns"][sub_concern]

            browser.click_button_with_id(concern["id"])  # Ausweise
            browser.click_button_with_id(sub_concern["id"])  # Personalausweis - Antrag
            browser.click_button_with_id("WeiterButton")  # Weiter
            # browser.click_button_with_id("OKButton")  # OK
            browser.click_element(
                element=browser.get_element_with_attribute("name", "select_location")
            )  # Standort auswählen

            all_open_slots = browser.get_open_slots_for_one_office(
                office="BuergerServiceCenter-Mitte"
            )
    finally:
        browser.quit()

    return slots.add_concern_to_slots(all_open_slots, sub_concern["name"])
