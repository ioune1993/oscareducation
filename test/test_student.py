# -*- coding: latin-1 -*-
import unittest
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

# Run with "python3.5 *test name*.py"
URL_IMG = "https://i.imgur.com/UkiM2YH.jpg"
URL_HOMEPAGE = "http://127.0.0.1:8000"
URL_LOGIN = "http://127.0.0.1:8000/accounts/usernamelogin/"
URL_SCENARIO_CREATION = "http://127.0.0.1:8000/professor/train/create_scenario/"
URL_LIST_SCENARIO = "http://127.0.0.1:8000/professor/train/list_scenario/"
URL_LIST_STUDENT = "http://127.0.0.1:8000/professor/train/student_list_scenario/"
URL_CLASS = "http://127.0.0.1:8000/professor/lesson/2/#"
URL_VIDEO = "https://www.youtube.com/watch?v=2bjk26RwjyU"


class SampleTest(unittest.TestCase):
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

    def test_student_view(self):

        driver = self.driver
        self.click_element_css("a[href='/professor/lesson/2/']")
        self.click_element_css("a[href='#listscena']")
        self.click_element_id("addElement")

        self.fill_field("title", "test_title")
        self.fill_field("instructions", "test_instructions")

        self.scroll_bottom()
        self.click_element_id("addElementVideo")
        self.scroll_bottom()
        self.fill_field("vid_url", URL_VIDEO)
        self.click_element_id("addVid")

        self.scroll_bottom()

        self.click_element_id("addElementImg")
        self.scroll_bottom()
        self.fill_field("img_url", URL_IMG)
        self.click_element_id("addImg")
        time.sleep(1)

        self.scroll_bottom()

        self.click_element_id("addElementMcq")
        self.scroll_bottom()
        self.fill_field_css("input[class='titre_MCQ_Elem']", "Titre_MCQ")
        self.fill_field_css("textarea[class='question_MCQ_Elem']", "question")
        self.fill_field_css("input[class='answer1 answer']", "Reponse 1")
        self.fill_field_css("input[class='answer2 answer']", "Reponse 2")
        self.click_element_css("input[class='answer1isvalid']")
        # self.click_element_css("input[class='answer1_is_valid']")
        # self.scroll_bottom()
        # self.click_element_css("button[title='Ajouter une réponse']")
        # self.fill_field_css("input[class='answer3']", "Réponse 3")

        self.scroll_bottom()

        self.click_element_id("saveScenario")
        time.sleep(1)
        driver.get(URL_LIST_STUDENT)

        body_text = self.driver.find_element_by_tag_name('body').text
        self.assertTrue("test_title" in body_text)

        self.click_element_css("a[href^='/student/train/make_scenario/'")
        self.click_element_id("begin")
        self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "iframe[src='//www.youtube.com/embed/2bjk26RwjyU']"))
        self.click_element_id("nextElement")

        self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "img[src='https://i.imgur.com/UkiM2YH.jpg']"))
        self.click_element_id("nextElement")

        self.click_element_id("validateElement")
        self.assertTrue(self.is_text_in_body("Bonne(s) Réponse(s)!"))

    def tearDown(self):
        # close the browser window and clear test scenarios
        self.driver.get(URL_CLASS)
        self.click_element_css("a[href='#listscena']")
        if self.is_element_present(By.CSS_SELECTOR, "img[alt = 'Supprimer le scénario']"):
            self.click_element_css("img[alt = 'Supprimer le scénario']")
            time.sleep(1)
            self.driver.switch_to.alert.accept()
        self.driver.quit()

    def is_text_in_body(self, text):
        body_text = self.driver.find_element_by_tag_name('body').text
        return text in body_text

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

    def click_element_id(self, el_id):
        els = self.driver.find_elements_by_id(el_id)
        for el in els:
            if el.is_displayed():
                el.click()
                # ActionChains(self.driver).move_to_element(el).click(el).perform()

    def click_element_css(self, selector):
        els = self.driver.find_elements_by_css_selector(selector)
        for el in els:
            if el.is_displayed():
                el.click()
                # ActionChains(self.driver).move_to_element(el).click(el).perform()

    def scroll_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    def fill_field(self, el_id, text):
        els = self.driver.find_elements_by_id(el_id)
        for el in els:
            if el.is_displayed():
                el.clear()
                el.send_keys(text)

    def fieldText(self, el_id):
        el = self.driver.find_element_by_id(el_id)
        return el.get_attribute("value")

    def fill_field_css(self, el_css, text):
        el = self.driver.find_element_by_css_selector(el_css)
        el.clear()
        el.send_keys(text)


if __name__ == "__main__":
    unittest.main()
