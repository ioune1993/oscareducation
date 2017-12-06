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



class TestEditing(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(2)
        self.base_url = "http://127.0.0.1:8000/"
        self.login = login
        self.pwd = pwd

    def testPersistance(self):
        self.assertEqual(1,1)

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()


