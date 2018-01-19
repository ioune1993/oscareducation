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
        driver.find_element_by_id("id_username").send_keys("prof")
        driver.find_element_by_xpath("//input[@type='submit']").click()
        driver.find_element_by_id("id_password").send_keys("prof")
        driver.find_element_by_xpath("//input[@type='submit']").click()
	time.sleep(3)

	driver.find_element_by_link_text('Hankar').click()
        driver.find_element_by_link_text('Mes Tests').click()
        driver.find_element_by_css_selector('img.icon').click()
        driver.find_element_by_link_text('Ajouter un test en ligne').click()
	time.sleep(3)

	driver.find_element_by_id("test_name").send_keys("tr")
	driver.find_element_by_id("addSkillToTestButtonForStage9").click()
	driver.find_element_by_css_selector('[ng-click="addNewTest()"]').click()
	time.sleep(3)

	driver.find_element_by_link_text("nouveau").click()
	time.sleep(3)

        driver.find_element_by_id('exercice-html').send_keys("ffzffs")
        driver.find_element_by_css_selector('input.form-control.ng-pristine.ng-invalid.ng-invalid-required').click()
        select = Select(driver.find_element_by_xpath(" *//select[@ng-model = 'question.type']"))
        select.select_by_value('chart-piechart')
        driver.find_element_by_xpath(" *//input[@ng-model = 'question.instructions']").send_keys("sggdgs")
        driver.find_element_by_xpath(" *//input[@ng-model = 'answer.text']").send_keys("3")
	secteur = driver.find_element_by_id("sector")
	secteur.clear()
	ajouter = driver.find_element_by_css_selector('[onclick="chart_createPieChartFromForm()"]')
	ajouter.click()
	secteur.send_keys("90")
	nomScteur = driver.find_element_by_id("labelPie")
	nomScteur.clear()
	nomScteur.send_keys("rouge")
	ajouter.click()
	nomScteur.send_keys("r")
	ajouter.click()
	time.sleep(3)
	secteur.clear()
	secteur.send_keys("180")
	nomScteur.clear()
	nomScteur.send_keys("vert")
	time.sleep(3)
	ajouter.click()
	time.sleep(3)
	secteur.clear()
	secteur.send_keys("45")
	ajouter.click()
	#driver.find_element_by_css_selector('[onclick ="chart_deleteLastPie($(this))"]').click()
	#driver.find_element_by_css_selector('[onclick ="chart_deleteLastPie($(this))"]').click()
	time.sleep(4)
	driver.find_element_by_id("validate-yaml").click()
	time.sleep(3)
	driver.find_element_by_id("submit-pull-request").click()
	time.sleep(3)
	driver.find_element_by_xpath(" *//a[@class = 'btn btn-lg btn-primary']").click()
	time.sleep(3)
	driver.find_element_by_xpath(" *//a[@href = '/professor/lesson/134/test/']").click()
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
