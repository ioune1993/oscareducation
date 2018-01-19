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
        driver.find_element_by_xpath(" *//a[contains(.,'bartest_new')]").click()
        time.sleep(3)
        driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(3)
        ajouter = driver.find_element_by_css_selector('[onclick="chart_add($(this))"]')
        ajouter.click()
        time.sleep(3)
        barre = driver.find_element_by_id("newBarY")
        
        barre.clear()
        barre.send_keys("4")
        time.sleep(3)
        ajouter.click()
        time.sleep(3)
        
        barre.clear()
        barre.send_keys("5")
        time.sleep(3)
        ajouter.click()
        time.sleep(3)
        
        supprimer = driver.find_element_by_css_selector('[onclick="chart_deleteLast($(this))"]')
        supprimer.click()
        driver.find_element_by_xpath("//input[@value='Répondre']").click()
        time.sleep(10)
        
    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
