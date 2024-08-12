from src.browser import Browser
import src.constants as const
from src.constants import DUESSELDORF, DRESDEN, BREMEN
import src.slots as slots
from src.slots import Slot as Slot
import src.database as db
from datetime import datetime


def main():

    # duesseldorf()
    # bremen()
    dresden()


def dresden():
    dresden = get_open_slots_from_dresden(
        concern="personaldokumente", sub_concern="personalausweis_antrag"
    )

    slots.print_slots(dresden, "Dresden:")

    print(f"Found {len(dresden)} slots in Dresden")

    # save_slots_per_city(dresden, "Dresden")


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


def save_slots_per_city(currently_open_slots, city, now=datetime.now()):
    print(f"Saving slots for {city} at {now}")
    open, updated, new = db.update_slots(currently_open_slots, timestamp=now, city=city)

    slots.print_slots(open, "Open slots:")
    slots.print_slots(updated, "Updated slots:", "fail")
    slots.print_slots(new, "New slots:", "green")

    print(
        f"Open: {len(open)} Updated: {len(updated)} New: {len(new)} in {city} at {now}"
    )


if __name__ == "__main__":
    main()
