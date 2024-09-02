from src.browser import Browser
import src.constants as const
from src.constants import DUESSELDORF, DRESDEN, BREMEN, HANNOVER, WIESBADEN
import src.slots as slots
from src.slots import Slot as Slot
import src.database as db
from datetime import datetime


def main():

    # duesseldorf()
    # bremen()
    # dresden()
    # hannover()
    wiesbaden()


def wiesbaden():
    wiesbaden = get_open_slots_from_wiesbaden()

    slots.print_slots(wiesbaden, "Wiesbaden:")

    print(f"Found {len(wiesbaden)} slots in Wiesbaden")

    # save_slots_per_city(wiesbaden, "Wiesbaden")


def get_open_slots_from_wiesbaden() -> list[Slot]:
    all_open_slots = []

    with Browser() as browser:
        browser.land_first_page(url=WIESBADEN["base_url"])

    browser.get_element_with_attribute("_bl_2", "").send_keys(
        WIESBADEN["form_data"]["nachname"]
    )

    browser.get_element_with_attribute("_bl_3", "").send_keys(
        WIESBADEN["form_data"]["vorname"]
    )

    browser.get_element_with_attribute("_bl_4", "").send_keys(
        WIESBADEN["form_data"]["email"]
    )

    browser.get_element_with_attribute("_bl_5", "").send_keys(
        WIESBADEN["form_data"]["telefon"]
    )

    browser.click_button_with_id("ckbDatenschutz")

    browser.get_element_with_attribute("type", "submit").click()

    browser.get_element_by_css_selector("div.list-group > button:nth-child(1)").click()

    select_element = browser.get_element_with_attribute("_bl_9", "")

    browser.select_option_by_value(select_element, "1")

    browser.get_element_with_attribute("type", "submit").click()

    # iterate over every button in list-group
    for button in browser.get_elements_with_class("list-group-item"):
        print(button.text)
        # 24.09.2024 10:30 / Bürgerbüro Marktstraße

        # extract date and time
        date_time = button.text.split(" / ")[0]
        date = date_time.split(" ")[0]
        time = date_time.split(" ")[1]

        # convert date and time to datetime object
        date_time = datetime.strptime(date + " " + time, "%d.%m.%Y %H:%M")

        # extract office
        office = button.text.split(" / ")[1]

        # concern = WIESBADEN["concerns"]["personalausweis_antrag"]["name"]
        slot = Slot(office, date_time)

        all_open_slots.append(slot)

    return slots.add_concern_to_slots(all_open_slots, "Personalausweis - Antrag")


if __name__ == "__main__":
    main()
