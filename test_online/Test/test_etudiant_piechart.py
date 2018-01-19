# coding: utf-8

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re


class BlogDriver(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:8000/accounts/usernamelogin/"
        self.driver.get(self.base_url)

    def test_log_in(self):
        driver = self.driver
        driver.find_element_by_id("id_username").send_keys("pierre.mousse")
        driver.find_element_by_xpath("//input[@type='submit']").click()
        driver.find_element_by_id("id_password").send_keys("pierre")
        driver.find_element_by_xpath("//input[@type='submit']").click()
        time.sleep(3)
        driver.find_element_by_xpath(" *//a[contains(.,'pietest_new')]").click()
        time.sleep(3)
        driver.find_element_by_xpath("//button[@type='submit']").click() #Do this if it is the first time that he open the exercice page
        time.sleep(3)
        driver.find_element_by_xpath("//input[@type='submit']").click()
        time.sleep(3)
        
    def is_element_present(self, how, what):
    	try:
    		self.driver.find_element(by=how, value=what)
    	except NoSuchElementException, e:
    		return False
    	return True
    	
    def tearDown(self):
    	self.driver.quit()

if __name__ == "__main__":
    unittest.main()
