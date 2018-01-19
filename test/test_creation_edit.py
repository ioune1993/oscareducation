# -*- coding: utf-8 -*-
import unittest

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import *

# Run with "python *test name*.py" or whatever version of python selenium is installed on
# Need to create a professor named "professor" with password "professor"
# Need to create a user named "student" with password "student"
# Webpages may sometimes need to be cached for the tests to work, I'm unsure of why
# There needs to be no scenario in "professor"'s scenario list

URL_HOMEPAGE = "http://127.0.0.1:8000"
URL_LOGIN = "http://127.0.0.1:8000/accounts/usernamelogin/"
URL_SCENARIO_CREATION = "http://127.0.0.1:8000/professor/train/create_scenario/"
URL_LIST_SCENARIO = "http://127.0.0.1:8000/professor/train/list_scenario/"
URL_CLASS = "http://127.0.0.1:8000/professor/lesson/2/#"
URL_VIDEO = "https://www.youtube.com/watch?v=2bjk26RwjyU"


class SampleTest(unittest.TestCase):
    # Sets up the tests by creating a Firefox webdriver, and logging in oscar as "professor"
    def setUp(self):
        # create a new Chrome session
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        self.driver.get(URL_LOGIN)
        self.fill_field("id_username", "professor")
        self.click_element_css("input[value='Connexion']")
        self.fill_field("id_password", "professor")
        self.click_element_css("input[value='Connexion']")

    # Verifies that the scenarios are correctly saved with the new elements when edited
    def test_edit_scenario(self):
        self.click_element_css("a[href='/professor/lesson/2/']")
        self.click_element_css("a[href='#listscena']")
        self.click_element_id("addElement")

        scenario_title = "old_title"

        self.fill_field("title", scenario_title)
        self.fill_field("instructions", "test")

        self.scroll_bottom()
        self.click_element_id("saveScenario")
        self.click_element_css("img[alt = 'Editer le scénario']")

        self.fill_field("title", "new title")
        self.fill_field("instructions", "new instructions")

        self.scroll_bottom()
        self.click_element_id("addElementVideo")

        self.scroll_bottom()
        self.fill_field("vid_url", URL_VIDEO)
        self.click_element_id("addVid")

        self.scroll_bottom()
        self.click_element_id("saveScenario")

        self.click_element_css("img[alt = 'Editer le scénario']")
        self.assertTrue(self.field_text("title") == "new title")
        self.assertTrue(self.field_text("instructions") == "new instructions")
        self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "iframe[src = '//www.youtube.com/embed/2bjk26RwjyU']"))

    # Verifies that scenarios created are in the list of scenarios
    def test_creation(self):
        self.click_element_css("a[href='/professor/lesson/2/']")
        self.click_element_css("a[href='#listscena']")
        self.click_element_id("addElement")

        scenario_title = "test_title_abcdef"

        # Check if a rightly created scenario is in the list

        self.fill_field("title", scenario_title)
        self.fill_field("instructions", "test")
        self.scroll_bottom()
        self.click_element_id("saveScenario")
        body_text = self.driver.find_element_by_tag_name('body').text
        self.assertTrue(scenario_title in body_text)

    # Verifies that scenarios that are deleted are not in the list anymore
    def test_deletion(self):

        self.click_element_css("a[href='/professor/lesson/2/']")
        self.click_element_css("a[href='#listscena']")
        self.click_element_id("addElement")

        scenario_title = "toDelete"

        # Check if a rightly created scenario is in the list

        self.fill_field("title", scenario_title)
        self.fill_field("instructions", "test")
        self.scroll_bottom()
        self.click_element_id("saveScenario")
        self.click_element_css("img[alt = 'Supprimer le scénario']")
        self.driver.switch_to.alert.accept()
        time.sleep(1)
        body_text = self.driver.find_element_by_tag_name('body').text
        self.assertFalse(scenario_title in body_text)

    # Ends a test by deleting the created scenario (if there is one) and closing the driver
    def tearDown(self):
        self.driver.get(URL_CLASS)
        self.click_element_css("a[href='#listscena']")
        if self.is_element_present(By.CSS_SELECTOR, "img[alt = 'Supprimer le scénario']"):
            self.click_element_css("img[alt = 'Supprimer le scénario']")
            time.sleep(1)
            self.driver.switch_to.alert.accept()
        self.driver.quit()

    def is_element_present(self, how, what):
        """
        Helper method to confirm the presence of an element on page
        :params how: By locator type
        :params what: locator value
        """
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException:
            return False
        return True

    # Clicks on an element located by its ID
    def click_element_id(self, el_id):
        els = self.driver.find_elements_by_id(el_id)
        for el in els:
            if el.is_displayed():
                el.click()
                # ActionChains(self.driver).move_to_element(el).click(el).perform()

    # Clicks on an element located by a CSS locator
    def click_element_css(self, selector):
        els = self.driver.find_elements_by_css_selector(selector)
        for el in els:
            if el.is_displayed():
                el.click()
                # ActionChains(self.driver).move_to_element(el).click(el).perform()

    # Scrolls down to the bottom of the web page
    def scroll_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    # Fills an editable field with the argument
    def fill_field(self, el_id, text):
        els = self.driver.find_elements_by_id(el_id)
        for el in els:
            if el.is_displayed():
                el.clear()
                el.send_keys(text)

    # Returns the text of an element located by its ID
    def field_text(self, el_id):
        el = self.driver.find_element_by_id(el_id)
        return el.get_attribute("value")


if __name__ == "__main__":
    unittest.main()
