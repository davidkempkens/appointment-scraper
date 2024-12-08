import sqlite3
from scraper.browser import Browser
from repository.SlotRepository import SlotRepository

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
                    "reisepass_antrag": {
                        "id": "button-plus-315",
                        "name": "Reisepass - Antrag",
                    },
                },
            },
            "bescheinigungen": {
                "id": "header_concerns_accordion-170",
                "sub_concerns": {
                    "anmeldung": {
                        "id": "button-plus-367",
                        "name": "Anmeldung",
                    },
                    "ummeldung": {
                        "id": "button-plus-499",
                        "name": "Ummeldung",
                    },
                    "abmeldung": {
                        "id": "button-plus-391",
                        "name": "Abmeldung",
                    },
                    "meldebescheinigung": {
                        "id": "button-plus-501",
                        "name": "Meldebescheinigung",
                    },
                },
            },
        },
    },
}


def dresden(sub_concern="personalausweis_antrag"):

    # SlotRepository(db=sqlite3.connect("db/dresden.db")).reset_db()
    # return

    concern = "personaldokumente"

    if sub_concern in ["anmeldung", "ummeldung", "abmeldung", "meldebescheinigung"]:
        concern = "bescheinigungen"

    online_slots = get_open_slots_from_dresden(concern=concern, sub_concern=sub_concern)

    concern_name = DRESDEN["buergerbueros"]["concerns"][concern]["sub_concerns"][
        sub_concern
    ]["name"]

    slot_repo = SlotRepository(db=sqlite3.connect("db/dresden.db"))

    report = slot_repo.synchronize_slots(
        online_slots=online_slots, city="Dresden", concern=concern_name
    )

    slot_repo.print(report, city="Dresden", concern=concern_name)


def get_open_slots_from_dresden(concern, sub_concern):
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
                office_window_handles,
                city="Dresden",
                concern=sub_concern["name"],
            )
    finally:
        browser.quit()

    return all_open_slots
