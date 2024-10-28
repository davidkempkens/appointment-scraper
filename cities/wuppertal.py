import sqlite3
from scraper.browser import Browser
from repository.SlotRepository import SlotRepository

WUPPERTAL = {
    "base_url": "https://www.wuppertal.de/rathaus-buergerservice/buergerservice/online-terminreservierung-ema.php",
    "concerns": {
        "abmeldung": {
            "id": "ABM-1568-mittermin",
            "name": "Abmeldung",
        },
    },
}


def wuppertal(concern):
    print("Wuppertal")
    print(concern)
    online_slots = get_open_slots_from_wuppertal(concern)


def get_open_slots_from_wuppertal(concern):
    all_open_slots = []

    try:
        with Browser(headless=False) as browser:
            browser.land_first_page(url=WUPPERTAL["base_url"])
            cookie_button = browser.get_element_with_attribute(
                "class", "SP-CookieUsageNotification__ok"
            )
            browser.click_element(cookie_button)
            # select = browser.get_element_with_id("ABM-1568-mittermin")
            select = browser.get_element_by_css_selector("#ABM-1568-mittermin")
            # ABM-1568-mittermin

            browser.select_option_by_value(select, "1")

    except Exception as e:
        print(f"Error: {e}")
        raise e

    return all_open_slots
