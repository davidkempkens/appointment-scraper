from src.browser import Browser
import src.slots as slots
from src.slots import Slot as Slot
import src.database as db

DRESDEN = {
    "offices": {
        "Bürgerbüro Altstadt (barrierefrei)": "Altstadt",
        "Bürgerbüro Blasewitz (Teilweise barrierefrei)": "Blasewitz",
        "Meldestelle Cossebaude (barrierefrei)": "Cossebaude",
        "Bürgerbüro Cotta (Teilweise barrierefrei)": "Cotta",
        "Junioramt": "Junioramt",
        "Bürgerbüro Klotzsche (Teilweise barrierefrei)": "Klotzsche",
        "Meldestelle Langebrück (barrierefrei)": "Langenbrueck",
        "Bürgerbüro Leuben": "Leuben",
        "Bürgerbüro Neustadt (barrierefrei)": "Neustadt",
        "Bürgerbüro Pieschen": "Pieschen",
        "Bürgerbüro Plauen (Teilweise barrierefrei)": "Plauen",
        "Bürgerbüro Prohlis (barrierefrei)": "Prohlis",
        "Meldestelle Weixdorf": "Weixdorf",
    },
    "base_url": "https://termine-buergerbuero.dresden.de/select2?md=2",
    "buergerbueros": {
        "name": "Bürgerbüros",
        "concerns": {
            "personaldokumente": {
                "id": "header_concerns_accordion-172",
                "sub_concerns": {
                    "personalausweis_antrag": {
                        "id": "button-plus-317",
                        "name": "Personalausweis - Antrag",
                    },
                },
            }
        },
    },
}


def dresden():
    dresden = get_open_slots_from_dresden(
        concern="personaldokumente", sub_concern="personalausweis_antrag"
    )

    db.save_slots_per_city(dresden, "Dresden")


def get_open_slots_from_dresden(concern, sub_concern) -> list[Slot]:
    all_open_slots = []

    try:
        with Browser() as browser:
            browser.land_first_page(url=DRESDEN["base_url"])
            browser.click_button_with_id("cookie_msg_btn_no")  # Decline Cookies

            area = DRESDEN["buergerbueros"]
            concern = area["concerns"][concern]
            sub_concern = concern["sub_concerns"][sub_concern]

            browser.click_button_with_id(concern["id"])  # Ausweise
            browser.click_button_with_id(sub_concern["id"])  # Personalausweis - Antrag

            browser.click_button_with_id("WeiterButton")  # Weiter
            browser.click_button_with_id("OKButton")  # OK

            # get all offices
            office_elements = browser.get_all_h3_elements()
            office_window_handles = browser.open_offices_in_new_tabs(
                office_elements, city=DRESDEN
            )

            all_open_slots = browser.get_open_slots_from_tabs_for_all_offices(
                office_window_handles
            )
    finally:
        browser.quit()

    return slots.add_concern_to_slots(all_open_slots, sub_concern["name"])
