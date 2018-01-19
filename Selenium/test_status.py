import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.keys import Keys

class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_search_in_python_org(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/accounts/usernamelogin/")
        elem = driver.find_element_by_id("id_username")
        elem.send_keys("prof")
        elem.send_keys(Keys.RETURN)
        driver.find_element_by_class_name("btn").click()
        elem = driver.find_element_by_id("id_password")
        elem.send_keys("prof")
        elem.send_keys(Keys.RETURN)
        driver.find_element_by_class_name("btn").click()
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "stat"))
        )
        img = driver.find_element_by_id("statIcon")
        print(img.get_attribute('src'))
        assert "status" in img.get_attribute('src')

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
