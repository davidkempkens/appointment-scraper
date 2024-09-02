import sys
from src.browser import Browser

# import src.constants as const
from src.constants import DUESSELDORF, DRESDEN, BREMEN, HANNOVER, WIESBADEN
import src.slots as slots
from src.slots import Slot as Slot
import src.database as db
from datetime import datetime


def main():

    try:
        if len(sys.argv) > 1:
            city = sys.argv[1].lower()
            if city == "duesseldorf":
                duesseldorf()
            elif city == "dresden":
                dresden()
            elif city == "bremen":
                bremen()
            elif city == "hannover":
                hannover()
            elif city == "wiesbaden":
                wiesbaden()
            else:
                print("City not found")
        else:
            duesseldorf()
            dresden()
            bremen()
            hannover()
            wiesbaden()

    except Exception as e:
        print(e)


def bremen():
    bremen = get_open_slots_from_bremen(
        concern="ausweise", sub_concern="personalausweis_antrag"
    )

    db.save_slots_per_city(bremen, "Bremen")


def wiesbaden():
    wiesbaden = get_open_slots_from_wiesbaden()

    db.save_slots_per_city(wiesbaden, "Wiesbaden")


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


def hannover():
    hannover = get_open_slots_from_hannover(concern="personalausweis_antrag")

    db.save_slots_per_city(hannover, "Hannover")


def wiesbaden():
    wiesbaden = get_open_slots_from_wiesbaden()

    # slots.print_slots(wiesbaden, "Wiesbaden:")

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
