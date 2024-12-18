from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import os
from model.Slot import Slot
from bs4 import BeautifulSoup
from datetime import datetime


class Browser(webdriver.Chrome):
    def __init__(self, driver_path="chromedriver.exe", teardown=False, headless=True):

        self.driver_path = driver_path
        self.teardown = teardown
        self.original_window = None
        chrome_options = Options()
        if not self.teardown:
            chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--log-level=1")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        chrome_options.add_argument("--search-engine-choice-country")
        if headless:
            chrome_options.add_argument("--headless")

        super(Browser, self).__init__(options=chrome_options)

        # self.implicitly_wait(15)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self, url):
        self.get(url)

    def click_button_with_id(self, id, time=3):
        button = WebDriverWait(self, time).until(
            EC.element_to_be_clickable((By.ID, id))
        )
        button.click()

    def get_h3_containing_office_names(
        self,
        search_term="Bürgerbüro",
        time=5,
    ) -> list:
        office_elements = WebDriverWait(self, time).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, f"//*[contains(@title, '{search_term}')]")
            )
        )
        return office_elements

    def get_all_h3_elements(self, time=3) -> list:
        return WebDriverWait(self, time).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "h3"))
        )

    def open_offices_in_new_tabs(self, offices, city=None) -> dict[str, str]:

        self.original_window = self.current_window_handle
        # print(f"Original Window: {self.original_window}")

        # dictonary that stores the office name and the window handle of the new tab
        office_window_handles = {}

        for office in offices:
            if "Termine" in office.get_attribute("title"):

                # expand accordion item if not already expanded
                if "false" in office.get_attribute("aria-expanded"):
                    self.click_element(office)

                # get the office name
                full_office_name = office.get_attribute("title").split(",")[0]

                # click on the Button in the expanded accoridion item
                # with "Bürgerbüro Kaiserswerth auswählen"
                input_element = self.get_element_with_attribute(
                    "value", full_office_name + " auswählen"
                )

                # open the Terminübersicht in a new tab
                self.open_element_in_new_tab(input_element)

                # get the window handle of most recently opened tab
                for window in self.window_handles:
                    if window != self.original_window:
                        if window not in office_window_handles.values():
                            if city is not None:
                                stadtteil = city["offices"][full_office_name]
                            else:
                                stadtteil = full_office_name.split(" ")[-1]
                            office_window_handles[stadtteil] = window
        return office_window_handles

    def open_element_in_new_tab(self, element):
        webdriver.ActionChains(self).key_down(Keys.CONTROL).click(element).key_up(
            Keys.CONTROL
        ).perform()

        # return the window handle of the most recently opened tab
        return self.window_handles[-1]

    def click_element(self, element, time=3):
        WebDriverWait(self, time).until(EC.element_to_be_clickable(element)).click()

    def select_option_by_value(self, element, value, time=3):
        select = WebDriverWait(self, time).until(EC.element_to_be_clickable(element))
        select = Select(select)
        select.select_by_value(value)

    def get_element_with_attribute(self, attribute, value, time=3):
        return WebDriverWait(self, time).until(
            EC.element_to_be_clickable((By.XPATH, f"//*[@{attribute}='{value}']"))
        )

    def get_elements_with_class(self, class_name, time=3):
        try:
            return WebDriverWait(self, time).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, class_name))
            )
        except:
            return []

    def get_open_slots_from_tabs_for_all_offices(
        self,
        office_window_handles,
        city=None,
        concern=None,
    ) -> list[Slot]:

        # all open slots for all offices
        open_slots = []

        # iterate over all offices and their window handles
        for office, window in office_window_handles.items():

            # switch to the tab with the office
            self.switch_to.window(window)
            # get the open slots for the office as a list of tuples (office, date)
            open_slots_for_office = self.get_open_slots_for_one_office(
                office, city, concern
            )

            # add the open slots to the list of all open slots
            open_slots.extend(open_slots_for_office)

            # close the tab with the office
            self.close()

        # return the list of all open slots for all offices
        return open_slots

    def get_open_slots_for_one_office(self, office, city, concern) -> list[Slot]:

        open_slots = []

        # Get the page source and parse it with BeautifulSoup
        soup = BeautifulSoup(self.page_source, "html.parser")

        # Find all buttons with the class "suggest_btn"
        buttons = soup.find_all("button", class_="suggest_btn")

        if not buttons:
            return open_slots

        for button in buttons:

            # The button is disabled if the slot is already taken
            if button.has_attr("disabled"):
                continue

            # The title of the button is the time of the slot in the format "HH:MM"
            time = button.get("title")

            # Find the hidden input element with the name "date" in the parent form

            date = (
                button.find_parent("form").find("input", {"name": "date"}).get("value")
            )

            # Build datetime object from the day and the time
            timeslot = datetime.strptime(date + " " + time, "%Y%m%d %H:%M")

            # Add the office and the date to the list of open slots
            open_slots.append(Slot(office, city, timeslot, concern))

        # Return the list of open slots for this one office
        return open_slots