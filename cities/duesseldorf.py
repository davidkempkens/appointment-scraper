from scraper.browser import Browser
import slots.slots as slots
from slots.slots import Slot as Slot
import db.database as db

DUESSELDORF = {
    "offices": [
        "Benrath",
        "Bilk",
        "Dienstleistungszentrum",
        "Eller",
        "Garath",
        "Gerresheim",
        "Kaiserswerth",
        "Oberkassel",
        "Rath",
        "Unterbach",
        "Wersten/Holthausen",
    ],
    "base_url": "https://termine.duesseldorf.de",
    "einwohnerangelegenheiten": {
        "id": "buttonfunktionseinheit-4",
        "name": "Einwohnerangelegenheiten",
        "concerns": {
            "meldeangelegenheiten": {
                "id": "header_concerns_accordion-3532",
                "sub_concerns": {
                    "anmeldung": {
                        "id": "button-plus-2751",
                        "name": "Anmeldung in Düsseldorf",
                    },
                    "ummeldung": {
                        "id": "button-plus-315",
                        "name": "Ummeldung innerhalb Düsseldorf",
                    },
                    "adressaenderung": {
                        "id": "button-plus-2786",
                        "name": "Adressänderung Fahrzeugschein bei Ummeldung",
                    },
                    "abmeldung": {
                        "id": "button-plus-3165",
                        "name": "Abmeldung eines wohnsitzes",
                    },
                },
            },
            "ausweise": {
                "id": "header_concerns_accordion-3533",
                "sub_concerns": {
                    "personalausweis_antrag": {
                        "id": "button-plus-2816",
                        "name": "Personalausweis - Antrag",
                    },
                    "vorlaeufiger_personalausweis": {
                        "id": "button-plus-2838",
                        "name": "Vorläufiger Personalausweis - Antrag",
                    },
                    "personalausweis_pin": {
                        "id": "button-plus-2852",
                        "name": "Personalausweis - Neusetzung PIN",
                    },
                    "reisepass_antrag": {
                        "id": "button-plus-2863",
                        "name": "Reisepass - Antrag",
                    },
                    "vorlaeufiger_reisepass": {
                        "id": "button-plus-2886",
                        "name": "Vorläufiger Reisepass - Antrag",
                    },
                },
            },
            "bescheinigungen": {
                "id": "header_concerns_accordion-3534",
                "sub_concerns": {
                    "beglaubigung": {
                        "id": "button-plus-2899",
                        "name": "Amtliche Beglaubigung",
                    },
                    "unterschriftsbeglaubigung": {
                        "id": "button-plus-2910",
                        "name": "Unterschriftsbeglaubigung",
                    },
                    "meldebescheinigung": {
                        "id": "button-plus-3158",
                        "name": "Meldebescheinigung",
                    },
                    "melderegisterauskunft": {
                        "id": "button-plus-2940",
                        "name": "Melderegisterauskunft",
                    },
                },
            },
        },
    },
}


def duesseldorf():
    duesseldorf = get_open_slots_from_duesseldorf(
        area="einwohnerangelegenheiten",
        concern="ausweise",
        sub_concern="personalausweis_antrag",
    )
    db.save_slots_per_city(duesseldorf, "Duesseldorf")


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
