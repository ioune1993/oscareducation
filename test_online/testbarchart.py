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

	driver.find_element_by_id("test_name").send_keys("bartest")
	driver.find_element_by_id("addSkillToTestButtonForStage9").click()
	driver.find_element_by_css_selector('[ng-click="addNewTest()"]').click()
	time.sleep(3)

	driver.find_element_by_link_text("nouveau").click()
	time.sleep(1)

        driver.find_element_by_id('exercice-html').send_keys("ffzffs")
        driver.find_element_by_css_selector('input.form-control.ng-pristine.ng-invalid.ng-invalid-required').click()
        select = Select(driver.find_element_by_xpath(" *//select[@ng-model = 'question.type']"))
        select.select_by_value('chart-barchart')
        driver.find_element_by_xpath(" *//input[@ng-model = 'question.instructions']").send_keys("sggdgs")
        driver.find_element_by_xpath(" *//input[@ng-model = 'answer.text']").send_keys("3")
        time.sleep(3)
        bar = driver.find_element_by_id("barGraphX")
        bar.clear()
        bar.send_keys("orange")
        time.sleep(3)
        bar1 = driver.find_element_by_id("barGraphY")
        bar1.clear()
        bar1.send_keys("mangue")
        time.sleep(3)
        step = driver.find_element_by_id("stepX")
        step.clear()
        step.send_keys("2")
        step1 = driver.find_element_by_id("stepY")
        step1.clear()
        step1.send_keys("2")
        zer = driver.find_element_by_id("zeroX")
        zer.clear()
        zer.send_keys("-1")
        time.sleep(3)
        zer1 = driver.find_element_by_id("zeroY")
        zer1.clear()
        zer1.send_keys("-1")
        maxi = driver.find_element_by_id("maxX")
        maxi.clear()
        maxi.send_keys("10")
        time.sleep(3)
        maxi1 = driver.find_element_by_id("maxY")
        maxi1.clear()
        maxi1.send_keys("10")
        pres = driver.find_element_by_id("precisionValue")
        pres.clear()
        pres.send_keys("1")
        barre = driver.find_element_by_id("newBarY")
        barre.clear()
        driver.find_element_by_css_selector('[onclick="chart_btnUpdate($(this))"]').click()
        ajouter = driver.find_element_by_css_selector('[onclick="chart_add($(this))"]')
	ajouter.click()
	
	barre.send_keys("4")
	time.sleep(3)
	ajouter.click()
	time.sleep(3)
	barre.clear()
	barre.send_keys("5")
	time.sleep(3)
	ajouter.click()
	time.sleep(3)
	supprimer = driver.find_element_by_css_selector('[onclick="chart_deleteLastBar($(this))"]')
	supprimer.click()
	time.sleep(3)
	driver.find_element_by_id("validate-yaml").click()
	time.sleep(3)
	driver.find_element_by_id("submit-pull-request").click()
	time.sleep(3)
	driver.find_element_by_xpath(" *//a[@class = 'btn btn-lg btn-primary']").click()
	time.sleep(3)
	driver.find_element_by_xpath(" *//a[contains(.,'Accéder au récapitulatif du test')]").click()
	time.sleep(3)
        
    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
