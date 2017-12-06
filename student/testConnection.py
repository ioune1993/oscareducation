# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re


login = "eleve.eleve"
pwd = "eleve"

loginProf = "prof"
pwdProf = "prof"

n1 = "22"  # Number of a test that we have finished
n2 = "38" # Number of a test allowed.
n3 = "27" # Number of a test that we have not finished
n4 = "21" # Number of a test. Used to test the access without logging
n5 = "28"
n6 = "134" # Number of lesson
n7 = 1


class TestStudentJS(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(2)
        self.base_url = "http://127.0.0.1:8000/"
        self.login = login
        self.pwd = pwd

    # The user try to access to the student dashboard
    def testWithoutLoggingProf(self):
        driver = self.driver
        driver.get("http://localhost:8000/student/dashboard/")
        self.assertEqual(driver.current_url,"http://localhost:8000/accounts/login/?next=/student/dashboard/") # The user is redirected

    # The user try to access to the professor dashboard
    def testWithoutLoggingProf(self):
        driver = self.driver
        driver.get("http://localhost:8000/professor/dashboard/")
        self.assertEqual(driver.current_url,"http://localhost:8000/accounts/login/?next=/professor/dashboard/") # The user is redirected

    # We test to access to student dashboard with prof account
    def testProfToStudent(self):
        driver = self.driver
        # Connection
        wait = WebDriverWait(driver, 2)
        driver.get(self.base_url + "accounts/usernamelogin/")
        page_source = driver.page_source
        element = re.search(r'input .* id="id_username"', page_source)
        self.assertNotEqual(element, None)

        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys(loginProf)
        driver.find_element_by_css_selector("input.btn.btn-primary").click()
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys(pwdProf)
        driver.find_element_by_css_selector("input.btn.btn-primary").click()
        driver.get("http://127.0.0.1:8000/student/dashboard/")
        self.assertEqual(driver.current_url,"http://127.0.0.1:8000/accounts/login/?next=/student/dashboard/")

    # We try to access to professor dashboard with student account
    def testStudentToProf(self):
        driver = self.driver
        # Connection
        wait = WebDriverWait(driver, 2)
        driver.get(self.base_url + "accounts/usernamelogin/")
        page_source = driver.page_source
        element = re.search(r'input .* id="id_username"', page_source)
        self.assertNotEqual(element, None)

        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys(login)
        driver.find_element_by_css_selector("input.btn.btn-primary").click()
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys(pwd)
        driver.find_element_by_css_selector("input.btn.btn-primary").click()
        driver.get("http://127.0.0.1:8000/professor/dashboard/")
        self.assertEqual(driver.current_url,"http://127.0.0.1:8000/accounts/login/?next=/professor/dashboard/")


    def testBasic(self):
        """self.driver.get("http://localhost:8000/")
        self.driver.find_element("bs-example-navbar-collapse-1").click()
        page_url = self.driver.current_url
        self.assertEqual(page_url, 'http://localhost:8000/accounts/')"""
        driver = self.driver
        wait = WebDriverWait(driver, 2)

        driver.get(self.base_url + "accounts/usernamelogin/")

        page_source = driver.page_source
        element = re.search(r'input .* id="id_username"', page_source)
        self.assertNotEqual(element, None)

        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys(self.login)
        driver.find_element_by_css_selector("input.btn.btn-primary").click()
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys(self.pwd)
        driver.find_element_by_css_selector("input.btn.btn-primary").click()
        self.assertEqual(driver.current_url,"http://127.0.0.1:8000/student/dashboard/")
        ##driver.find_element_by_xpath("//a[@href='/student/test/' + n1+ ' /']").click()
        #driver.find_element_by_class_name("panel-body")


    # We try to access a test that the student had already passed.
    def testFinished(self):
        driver = self.driver
        wait = WebDriverWait(driver, 2)
        driver.get(self.base_url + "accounts/usernamelogin/")
        page_source = driver.page_source
        element = re.search(r'input .* id="id_username"', page_source)
        self.assertNotEqual(element, None)
        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys(self.login)
        driver.find_element_by_css_selector("input.btn.btn-primary").click()
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys(self.pwd)
        driver.find_element_by_css_selector("input.btn.btn-primary").click()
        driver.get("http://127.0.0.1:8000/student/test/" +n1+"/")
        #driver.find_element_by_class_name("panel-body")
        self.assertIn("!\nRevenir ",driver.find_element_by_class_name("panel-body").text)


    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
