# coding: utf-8

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re
#import HTMLTestRunner


class BlogDriver(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
		#go to the home page to loggin as teacher because this test is for teach to create a barchart test
        self.base_url = "http://127.0.0.1:8000/accounts/usernamelogin/"
        self.driver.get(self.base_url)

    def test_Teachercreatebartest(self):
        driver = self.driver
        self.assertTrue(driver.current_url.endswith("/accounts/usernamelogin/"))
		
		#the teacher log in with is username and the password associate
        driver.find_element_by_id("id_username").send_keys("prof")
        driver.find_element_by_xpath("//input[@type='submit']").click()
        driver.find_element_by_id("id_password").send_keys("prof")
        time.sleep(3)
        i = 0
        url = driver.current_url
        while(i < 1000 and url == driver.current_url):
        	driver.find_element_by_xpath("//input[@type='submit']").click()
        	i += 1
        time.sleep(3)
        self.assertTrue(driver.current_url.endswith("/professor/dashboard/"))
        
        #The teacher enter the class and add a new test for his student
        i = 0
        url = driver.current_url
        while(i < 1000 and url == driver.current_url):
        	driver.find_element_by_link_text('Hankar').click()
        	i += 1
        time.sleep(1)
        self.assertTrue(driver.current_url.endswith("/professor/lesson/134/"))
        
        i = 0
        url = driver.current_url
        while(i < 1000 and url == driver.current_url):
        	driver.find_element_by_link_text('Mes Tests').click()
        	i += 1
        	
        time.sleep(1)
        self.assertTrue(driver.current_url.endswith("/test/"))
		
    	i = 0
    	url = driver.current_url
    	while(i < 1000 and url == driver.current_url):
    		driver.find_element_by_css_selector('img.icon').click()
    		i += 1
    	
    	time.sleep(1)
    	self.assertTrue(driver.current_url.endswith("/test/add/"))
		
        i = 0
        url = driver.current_url
        while(i < 1000 and url == driver.current_url):
        	driver.find_element_by_link_text('Ajouter un test en ligne').click()
        	i += 1
        	
        time.sleep(3)
        self.assertTrue(driver.current_url.endswith("/test/online/add/"))
        
        #here the teacher give the name of his test 
        driver.find_element_by_id("test_name").send_keys("pietest_new")
        driver.find_element_by_id("addSkillToTestButtonForStage9").click()
        time.sleep(3)
        
        i = 0
        url = driver.current_url
        while(i < 1000 and url == driver.current_url):
        	driver.find_element_by_css_selector('[ng-click="addNewTest()"]').click()
        	i += 1
        	
        time.sleep(5)
        
        
        i = 0
        url = driver.current_url
        while(i < 1000 and url == driver.current_url):
        	self.assertTrue(driver.current_url.endswith("/modify/"))
        	driver.find_element_by_link_text("nouveau").click()
        	i += 1
        	
        time.sleep(5)
        self.assertTrue("/professor/exercices/validation_form/" in driver.current_url)
        
        #here begin our module, create a piechart
        driver.find_element_by_id('exercice-html').send_keys("ffzffs")
        driver.find_element_by_css_selector('input.form-control.ng-pristine.ng-invalid.ng-invalid-required').click()
        select = Select(driver.find_element_by_xpath(" *//select[@ng-model = 'question.type']"))
        select.select_by_value('chart-piechart')
        driver.find_element_by_xpath(" *//input[@ng-model = 'question.instructions']").send_keys("sggdgs")
        driver.find_element_by_xpath(" *//input[@ng-model = 'answer.text']").send_keys("3")
        secteur = driver.find_element_by_id("sector")
        ajouter = driver.find_element_by_css_selector('[onclick="chart_createPieChartFromForm()"]')
        nomScteur = driver.find_element_by_id("labelPie")
        
        secteur.clear()
        secteur.send_keys("90")
        nomScteur.clear()
        nomScteur.send_keys("rouge")
        time.sleep(5)
        ajouter.click()
        time.sleep(10)
        
        secteur.clear()
        secteur.send_keys("180")
        nomScteur.clear()
        nomScteur.send_keys("vert")
        time.sleep(5)
        ajouter.click()
        time.sleep(5)
        
        #if we had a pie and the sum is greather than 360 and exception will be raise
        secteur.clear()
        secteur.send_keys("45")
        nomScteur.clear()
        nomScteur.send_keys("vert")
        time.sleep(5)
        ajouter.click()
        time.sleep(5)
        
        driver.find_element_by_css_selector('[onclick ="chart_deleteLastPie($(this))"]').click()
        #driver.find_element_by_css_selector('[onclick ="chart_deleteLastPie($(this))"]').click()
        time.sleep(10)
        driver.find_element_by_id("validate-yaml").click()
        time.sleep(10)
        
        i = 0
        url = driver.current_url
        while(i < 1000 and url == driver.current_url):
        	driver.find_element_by_id("submit-pull-request").click()
        	i += 1
        
        time.sleep(10)
        self.assertTrue("/modify/#" in driver.current_url)
        
        i = 0
        url = driver.current_url
        while(i < 1000 and url == driver.current_url):
        	driver.find_element_by_xpath(" *//a[@class = 'btn btn-lg btn-primary']").click()
        	i += 1
			
		time.sleep(5)
		#self.assertTrue("/modify/" not in driver.current_url)
		
		i = 0
		url = driver.current_url
		while(i < 1000 and url == driver.current_url):
			driver.find_element_by_xpath(" *//a[@href = '/professor/lesson/134/test/']").click()
			i += 1
			
		time.sleep(5)
		self.assertTrue(driver.current_url.endswith("/test/"))

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
