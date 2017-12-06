import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from features import Browser


class AddStudentClassPageLocator(object):
    # Login page elements locator
    URL = r'/professor/lesson/[0-9]+/student/add/'
    SUBMIT = (By.XPATH, "//button[@type='submit']")
    FIRST_NAME_0_INPUT = (By.XPATH, "//input[@name='first_name_0']")
    LAST_NAME_0_INPUT = (By.XPATH, "//input[@name='last_name_0']")
    FIRST_NAME_1_INPUT = (By.XPATH, "//input[@name='first_name_1']")
    LAST_NAME_1_INPUT = (By.XPATH, "//input[@name='last_name_1']")


class AddStudentClassPage(Browser):
    def navigate(self, base_url):
        self.driver.get(base_url + AddStudentClassPageLocator.URL)

    def currently_on_this_page(self):
        return re.search(AddStudentClassPageLocator.URL, self.driver.current_url)

    # Login page actions

    def fill_student_1_first_name(self, text):
        self.fill(text, *AddStudentClassPageLocator.FIRST_NAME_0_INPUT)

    def fill_student_1_last_name(self, text):
        self.fill(text, *AddStudentClassPageLocator.LAST_NAME_0_INPUT)

    def fill_student_2_first_name(self, text):
        self.fill(text, *AddStudentClassPageLocator.FIRST_NAME_1_INPUT)

    def fill_student_2_last_name(self, text):
        self.fill(text, *AddStudentClassPageLocator.LAST_NAME_1_INPUT)

    def submit(self):
        self.click_element(*AddStudentClassPageLocator.SUBMIT)
