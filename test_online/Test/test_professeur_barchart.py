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
        self.assertTrue(driver.current_url.endswith("/accounts/usernamelogin/"))
        
        #the teacher log in with is username and the password associate
        driver.find_element_by_id("id_username").send_keys("prof")
        driver.find_element_by_xpath("//input[@type='submit']").click()
        driver.find_element_by_id("id_password").send_keys("prof")
        driver.find_element_by_xpath("//input[@type='submit']").click()
        self.assertTrue(driver.current_url.endswith("/professor/dashboard/"))
        
        #here he enter the class and add a new test for his student
        driver.find_element_by_link_text('Hankar').click()
        driver.find_element_by_link_text('Mes Tests').click()
        driver.find_element_by_css_selector('img.icon').click()
        driver.find_element_by_link_text('Ajouter un test en ligne').click()
        time.sleep(3)
        driver.find_element_by_id("test_name").send_keys("bartest_new")
        driver.find_element_by_id("addSkillToTestButtonForStage9").click()
        time.sleep(3)
        
        i = 0
        url = driver.current_url
        while(i < 1000 and url == driver.current_url):
        	driver.find_element_by_css_selector('[ng-click="addNewTest()"]').click()
        	i += 1
        	
        time.sleep(5)
        
        element = driver.find_element_by_link_text("nouveau")
        self.assertTrue(driver.current_url.endswith("/modify/"))
        if element.is_displayed():
        	element.click()
        	print("Found the link!")
        else:
        	print("not found")
        
        time.sleep(10)
        
        #creation of the barchart with all the integer needed and names
        driver.find_element_by_id('exercice-html').send_keys("ffzffs")
        driver.find_element_by_css_selector('input.form-control.ng-pristine.ng-invalid.ng-invalid-required').click()
        select = Select(driver.find_element_by_xpath(" *//select[@ng-model = 'question.type']"))
        select.select_by_value('chart-barchart')
        locators = [ (By.XPATH, "*//input[@ng-model = 'question.instructions']"), (By.XPATH, "*//input[@ng-model = 'answer.text']")]
        for by, value in locators:
        	try:
        		driver.find_element(by, value).send_keys("sssgee")
        		driver.find_element(by, value).send_keys("3")
        	except NoSuchElementException:
        		return false
        	pass
        
        #driver.find_element_by_xpath(" *//input[@ng-model = 'question.instructions']").send_keys("sggdgs")
        #driver.find_element_by_xpath(" *//input[@ng-model = 'answer.text']").send_keys("3")
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
        time.sleep(10)
        ajouter.click()
        time.sleep(3)
        supprimer = driver.find_element_by_css_selector('[onclick="chart_deleteLastBar($(this))"]')
        supprimer.click()
        time.sleep(3)
        driver.find_element_by_id("validate-yaml").click()
        time.sleep(10)
        driver.find_element_by_id("submit-pull-request").click()
        time.sleep(10)
        driver.find_element_by_xpath(" *//a[@class = 'btn btn-lg btn-primary']").click()
        time.sleep(10)
        driver.find_element_by_link_text("Retour aux tests").click()
        time.sleep(3)
        
	def tearDown(self):
		self.driver.quit()

if __name__ == "__main__":
    unittest.main()
