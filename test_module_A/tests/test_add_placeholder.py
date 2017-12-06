# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re, customwebdriver

class TestAddPlaceholder(unittest.TestCase):
    def setUp(self):
        self.driver = customwebdriver.customwebdriver()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_add_placeholder(self):

        driver = self.driver
        wait = WebDriverWait(driver, 10)

        driver.get(self.base_url + "accounts/usernamelogin/")

        page_source = driver.page_source
        element = re.search(r'input .* id="id_username"', page_source)
        self.assertNotEqual(element, None)

        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys("prof")
        driver.find_element_by_css_selector("input.btn.btn-primary").click()
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("prof")
        driver.find_element_by_css_selector("input.btn.btn-primary").click()
        driver.find_element_by_xpath("//a[@href='/professor/lesson/134/']").click()
        driver.get("http://127.0.0.1:8000/professor/exercices/validation_form/#?for_test_exercice=48&code=S23aII")
        Select(driver.find_element_by_xpath("//li/div/div/div/select")).select_by_visible_text(u"Question à trous")
        driver.find_element_by_id("blank-text").clear()
        text = driver.find_element_by_id("blank-text").get_attribute('value')
        self.assertEqual(text,"")
        driver.find_element_by_css_selector("button.btn.btn-success").send_keys(Keys.ENTER)
        text = driver.find_element_by_id("blank-text").get_attribute('value')
        self.assertEqual(text,"#[1]#")
        driver.find_element_by_css_selector("button.btn.btn-success").send_keys(Keys.ENTER)
        text = driver.find_element_by_id("blank-text").get_attribute('value')
        self.assertEqual(text,"#[1]##[2]#")

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True

    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True

    def tearDown(self):
        self.driver.close()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
