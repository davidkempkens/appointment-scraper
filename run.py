import sys
from src.browser import Browser

# import src.constants as const
from src.constants import DUESSELDORF, DRESDEN, BREMEN
import src.slots as slots
from src.slots import Slot as Slot
import src.database as db
from datetime import datetime


def main():

    if len(sys.argv) > 1:
        city = sys.argv[1].lower()
        if city == "duesseldorf":
            duesseldorf()
        elif city == "dresden":
            dresden()
        elif city == "bremen":
            bremen()
        else:
            print("City not found")
    else:
        duesseldorf()
        dresden()
        bremen()


def bremen():
    bremen = get_open_slots_from_bremen(
        concern="ausweise", sub_concern="personalausweis_antrag"
    )

    db.save_slots_per_city(bremen, "Bremen")


def duesseldorf():
    duesseldorf = get_open_slots_from_duesseldorf(
        area="einwohnerangelegenheiten",
        concern="ausweise",
        sub_concern="personalausweis_antrag",
    )
    db.save_slots_per_city(duesseldorf, "Duesseldorf")


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


def get_open_slots_from_duesseldorf(area, concern, sub_concern) -> list[Slot]:
    all_open_slots = []

    try:
        with Browser() as browser:
            browser.land_first_page(url=DUESSELDORF["base_url"])
            browser.click_button_with_id("cookie_msg_btn_no")  # Decline Cookies

            area = DUESSELDORF[area]
            concern = area["concerns"][concern]
            sub_concern = concern["sub_concerns"][sub_concern]

            browser.click_button_with_id(area["id"])
            browser.click_button_with_id(concern["id"])
            browser.click_button_with_id(sub_concern["id"])

            browser.click_button_with_id("WeiterButton")  # Weiter
            browser.click_button_with_id("OKButton")  # OK

            # get all offices
            offices = browser.get_h3_containing_office_names()
            office_window_handles = browser.open_offices_in_new_tabs(offices)

            all_open_slots = browser.get_open_slots_from_tabs_for_all_offices(
                office_window_handles
            )
    finally:
        browser.quit()

    return slots.add_concern_to_slots(all_open_slots, sub_concern["name"])


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


if __name__ == "__main__":
    main()
