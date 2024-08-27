from src.browser import Browser
import src.constants as const
from src.constants import DUESSELDORF, DRESDEN, BREMEN, HANNOVER
import src.slots as slots
from src.slots import Slot as Slot
import src.database as db
from datetime import datetime


def main():

    # duesseldorf()
    # bremen()
    # dresden()
    hannover()


def hannover():
    hannover = get_open_slots_from_hannover()

    slots.print_slots(hannover, "Hannover:")

    print(f"Found {len(hannover)} slots in Hannover")

    # save_slots_per_city(hannover, "Hannover")


def get_open_slots_from_hannover() -> list[Slot]:
    all_open_slots = []

    with Browser() as browser:
        browser.land_first_page(url=HANNOVER["base_url"])

        # enter postal code because it is prompted
        browser.get_element_with_id("input-field").send_keys(HANNOVER["plz"])

        # select Personalausweis
        select_element = browser.get_element_with_id(
            "service_ede3dafc-4941-4e08-9526-bd70d77160ce"
        )
        browser.select_option_by_value(select_element, "1")
        browser.get_element_with_attribute("data-testid", "button_next").click()

        browser.click_button_with_id("locations_selected_all_top")
        browser.click_button_with_id("next-button")

        slots_element = browser.get_elements_with_class("timeslot_cards")
        all_open_slots = browser.get_open_slots_from_element(slots_element)

        browser.quit()

    return slots.add_concern_to_slots(all_open_slots, "Personalausweis - Antrag")


def get_open_slots_from_dresden(concern, sub_concern) -> list[Slot]:
    all_open_slots = []

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
        print(len(office_elements))
        office_window_handles = browser.open_offices_in_new_tabs(
            office_elements, city=DRESDEN
        )

        all_open_slots = browser.get_open_slots_from_tabs_for_all_offices(
            office_window_handles
        )
        browser.quit()

        for slot in all_open_slots:
            slot.concern = (
                sub_concern["name"] if sub_concern["name"] else sub_concern["id"]
            )

    return all_open_slots


if __name__ == "__main__":
    main()
