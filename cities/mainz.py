from scraper.browser import Browser
import slots.slots as slots
from slots.slots import Slot as Slot
import db.database as db
from datetime import datetime


MAINZ = {
    "base_url": "https://termine-reservieren.de/termine/buergeramt.mainz/select2?md=2",
    "concerns": {
        "personalausweis_antrag": {
            "id": "button-plus-750",
            "name": "Personalausweis - Antrag",
        },
    },
    "checkboxes_ids": [
        "doclist_item_750_49389",
        "doclist_item_750_49390",
        "doclist_item_750_49368",
        "doclist_item_750_49393",
        "doclist_item_750_49391",
        "doclist_item_750_49392",
        "doclist_item_750_49394",
    ],
    "checkboxes_xpath": [
        '//*[@id="TevisDialog"]/div/div/div[2]/div/div[1]/div/label',
        '//*[@id="TevisDialog"]/div/div/div[2]/div/div[2]/div/label',
        '//*[@id="TevisDialog"]/div/div/div[2]/div/div[3]/div/label',
        '//*[@id="TevisDialog"]/div/div/div[2]/div/div[4]/div/label',
        '//*[@id="TevisDialog"]/div/div/div[2]/div/div[5]/div/label',
        '//*[@id="TevisDialog"]/div/div/div[2]/div/div[6]/div/label',
        '//*[@id="TevisDialog"]/div/div/div[2]/div/div[7]/div/label',
    ],
    "offices": {
        "Marienborn": {
            "name": "Ortsverwaltung Marienborn (barrierefrei)",
            "value": "Ortsverwaltung Marienborn (barrierefrei)  auswählen",
        },
        "Finthen": {
            "name": "Ortsverwaltung Finthen (barrierefrei)",
            "value": "Ortsverwaltung Finthen (barrierefrei)  auswählen",
        },
        "Hechtsheim": {
            "name": "Ortsverwaltung Hechtsheim (barrierefrei)",
            "value": "Ortsverwaltung Hechtsheim (barrierefrei)  auswählen",
        },
        "Weisenau": {
            "name": "Ortsverwaltung Weisenau (barrierefrei)",
            "value": "Ortsverwaltung Weisenau (barrierefrei)  auswählen",
        },
        "Ebersheim": {
            "name": "Ortsverwaltung Ebersheim (barrierefrei)",
            "value": "Ortsverwaltung Ebersheim (barrierefrei)  auswählen",
        },
        "Drais": {
            "name": "Ortsverwaltung Drais (barrierefrei)",
            "value": "Ortsverwaltung Drais (barrierefrei)  auswählen",
        },
        "Stadthaus": {
            "name": "Bürgerservice Stadthaus, Lauterenflügel (barrierefrei)",
            "value": "Bürgerservice Stadthaus, Lauterenflügel (barrierefrei) auswählen",
        },
        "Lerchenberg": {
            "name": "Ortsverwaltung Lerchenberg (barrierefrei)",
            "value": "Ortsverwaltung Lerchenberg (barrierefrei) auswählen",
        },
        "Gonsenheim": {
            "name": "Ortsverwaltung Gonsenheim (nicht barrierefrei)",
            "value": "Ortsverwaltung Gonsenheim (nicht barrierefrei)  auswählen",
        },
        "Hartenberg-Muenchfeld": {
            "name": "Ortsverwaltung Hartenberg-Münchfeld (barrierefrei)",
            "value": "Ortsverwaltung Hartenberg-Münchfeld (barrierefrei)  auswählen",
        },
        "Altstadt_Mainz": {
            "name": "Ortsverwaltung Altstadt (barrierefrei)",
            "value": "Ortsverwaltung Altstadt (barrierefrei)  auswählen",
        },
        "Laubenheim": {
            "name": "Ortsverwaltung Laubenheim (barrierefrei)",
            "value": "Ortsverwaltung Laubenheim (barrierefrei)  auswählen",
        },
        "Mombach": {
            "name": "Ortsverwaltung Mombach (barrierefrei)",
            "value": "Ortsverwaltung Mombach (barrierefrei)  auswählen",
        },
        "Bretzenheim": {
            "name": "Ortsverwaltung Bretzenheim (nicht barrierefrei)",
            "value": "Ortsverwaltung Bretzenheim (nicht barrierefrei)  auswählen",
        },
        "Oberstadt": {
            "name": "Ortsverwaltung Oberstadt (nicht barrierefrei)",
            "value": "Ortsverwaltung Oberstadt (nicht barrierefrei)  auswählen",
        },
        "Neustadt_Mainz": {
            "name": "Ortsverwaltung Neustadt (barrierefrei)",
            "value": "Ortsverwaltung Neustadt (barrierefrei)  auswählen",
        },
    },
}


def mainz():
    mainz = get_open_slots_from_mainz()

    db.save_slots_per_city(mainz, "Mainz")


def get_open_slots_from_mainz():

    all_open_slots = []

    with Browser() as browser:
        browser.land_first_page(MAINZ["base_url"])

        browser.click_button_with_id("cookie_msg_btn_no")  # Decline Cookies

        browser.click_button_with_id(MAINZ["concerns"]["personalausweis_antrag"]["id"])

        browser.click_button_with_id("WeiterButton")  # Weiter

        # for checkbox_id in MAINZ["checkboxes_ids"]:
        #     # browser.click_button_with_id(checkbox_id)
        #     browser.get_element_with_attribute("for", checkbox_id).click()

        for checkbox_xpath in MAINZ["checkboxes_xpath"]:
            browser.get_element_by_xpath(checkbox_xpath).click()

        browser.click_button_with_id("OKButton")  # OK

        open_tabs_offices = {}

        for office in MAINZ["offices"]:
            # print("Office: ", office)
            h3 = browser.get_h3_containing_office_names(
                search_term=MAINZ["offices"][office]["name"]
            )[0]

            if "Termine" in h3.get_attribute("title"):
                if "false" in h3.get_attribute("aria-expanded"):
                    browser.click_element(h3)

                input_element = browser.get_element_with_attribute(
                    "value", MAINZ["offices"][office]["value"], time=3
                )

                tab_to_office = browser.open_element_in_new_tab(input_element)

                open_tabs_offices[office] = tab_to_office

        for tab in open_tabs_offices:
            browser.switch_to.window(open_tabs_offices[tab])
            slots_for_one_office = browser.get_open_slots_for_one_office(tab)
            all_open_slots.extend(slots_for_one_office)
            browser.close()

    browser.quit()

    return slots.add_concern_to_slots(all_open_slots, "Personalausweis - Antrag")
