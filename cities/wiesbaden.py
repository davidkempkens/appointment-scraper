from scraper.browser import Browser
import slots.slots as slots
from slots.slots import Slot as Slot
import db.database as db
from datetime import datetime


WIESBADEN = {
    "base_url": "https://dtms.wiesbaden.de/DTMSTerminWeb",
    "form_data": {
        "nachname": "Mustermann",
        "vorname": "Max",
        "email": "max.mustermann@mail.de",
        "telefon": "01234567890",
    },
    "concerns": {
        "personalausweis_antrag": {
            "id": "service_ede3dafc-4941-4e08-9526-bd70d77160ce",
            "name": "Personalausweis - Antrag",
        },
    },
}


def wiesbaden():
    wiesbaden = get_open_slots_from_wiesbaden()

    db.save_slots_per_city(wiesbaden, "Wiesbaden")


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

        browser.get_element_by_css_selector(
            "div.list-group > button:nth-child(1)"
        ).click()

        select_element = browser.get_element_with_attribute("_bl_9", "")

        browser.select_option_by_value(select_element, "1")

        browser.get_element_with_attribute("type", "submit").click()

        # iterate over every button in list-group
        for button in browser.get_elements_with_class("list-group-item"):
            # 24.09.2024 10:30 / Bürgerbüro Marktstraße

            # extract date and time
            date_time = button.text.split(" / ")[0]
            date = date_time.split(" ")[0]
            time = date_time.split(" ")[1]

            # convert date and time to datetime object
            date_time = datetime.strptime(date + " " + time, "%d.%m.%Y %H:%M")

            # extract office
            office = button.text.split(" / ")[1]

            office = office.replace("Bürgerbüro ", "")

            slot = Slot(office, date_time)

            all_open_slots.append(slot)

        browser.quit()

    return slots.add_concern_to_slots(all_open_slots, "Personalausweis - Antrag")
