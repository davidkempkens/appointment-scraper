from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import os
import src.constants as const
import src.slots as slots
from src.slots import Slot as Slot
from bs4 import BeautifulSoup
from datetime import datetime


class Browser(webdriver.Chrome):
    def __init__(self, driver_path="chromedriver.exe", teardown=False):

        self.driver_path = driver_path
        self.teardown = teardown
        self.original_window = None
        chrome_options = Options()
        if not self.teardown:
            chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--log-level=1")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        chrome_options.add_argument("--search-engine-choice-country")

        super(Browser, self).__init__(options=chrome_options)

        # self.implicitly_wait(15)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self, url=const.DUESSELDORF_BASE_URL):
        self.get(url)

    def click_button_with_id(self, id, time=15):
        button = WebDriverWait(self, time).until(
            EC.element_to_be_clickable((By.ID, id))
        )
        button.click()

    def get_h3_containing_office_names(
        self,
        search_term="Bürgerbüro",
    ) -> list:
        office_elements = WebDriverWait(self, 15).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, f"//*[contains(@title, '{search_term}')]")
            )
        )
        return offices

    def open_offices_in_new_tabs(self, offices) -> dict[str, str]:

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
                office_name = office.get_attribute("title").split(",")[0]

                # click on the Button in the expanded accoridion item
                # with "Bürgerbüro Kaiserswerth auswählen"
                input_element = self.get_element_with_attribute(
                    "value", office_name + " auswählen"
                )

                # open the Terminübersicht in a new tab
                self.open_element_in_new_tab(input_element)

                # get the window handle of most recently opened tab
                for window in self.window_handles:
                    if window != self.original_window:
                        if window not in office_window_handles.values():
                            stadtteil = office_name.split(" ")[1]
                            office_window_handles[stadtteil] = window

        return office_window_handles

    def open_element_in_new_tab(self, element):
        webdriver.ActionChains(self).key_down(Keys.CONTROL).click(element).key_up(
            Keys.CONTROL
        ).perform()

    def click_element(self, element, time=15):
        WebDriverWait(self, time).until(EC.element_to_be_clickable(element)).click()

    def get_element_with_attribute(self, attribute, value):
        return WebDriverWait(self, 15).until(
            EC.element_to_be_clickable((By.XPATH, f"//*[@{attribute}='{value}']"))
        )

    def get_element_with_id(self, id):
        return WebDriverWait(self, 15).until(EC.element_to_be_clickable((By.ID, id)))

    def get_elements_with_class(self, class_name):
        return WebDriverWait(self, 15).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, class_name))
        )

    def get_open_slots_from_tabs_for_all_offices(
        self, office_window_handles
    ) -> list[Slot]:

        # all open slots for all offices
        open_slots = []

        # iterate over all offices and their window handles
        for office, window in office_window_handles.items():

            # switch to the tab with the office
            self.switch_to.window(window)
            # get the open slots for the office as a list of tuples (office, date)
            open_slots_for_office = self.get_open_slots_for_one_office(office)

            # add the open slots to the list of all open slots
            open_slots.extend(open_slots_for_office)

            # close the tab with the office
            self.close()

        # return the list of all open slots for all offices
        return open_slots

    def get_open_slots_for_one_office(self, office) -> list[Slot]:

        open_slots = []

        buttons = self.get_elements_with_class("suggest_btn")

        for button in buttons:

            # the button is disabled if the slot is already taken
            if button.get_attribute("disabled") == "true":
                # does not need to be saved
                continue

            # the title of the button is the time of the slot
            # in the format "HH:MM"
            time = button.get_attribute("title")

            # <form>
            #     <input type="hidden" name="date" value="20210826">
            #     ...
            #    <button class="suggest_btn" title="08:00" disabled>
            # </form>
            date = (
                button.find_element(By.XPATH, "..")
                .find_element(By.NAME, "date")
                .get_attribute("value")
            )

            # build datetime object from the day and the time
            slot = datetime.strptime(date + " " + time, "%Y%m%d %H:%M")

            # add the office and the date to the list of open slots
            open_slots.append(Slot(office, slot))

        # return the list of open slots for this one office
        return open_slots

    def check_if_element_exists(self, id, time=5):
        try:
            WebDriverWait(self, time).until(EC.presence_of_element_located((By.ID, id)))
            return True
        except:
            return False
