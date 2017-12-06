import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from features import Browser


class ClassPageLocator(object):
    # Login page elements locator
    URL = r'/professor/lesson/[0-9]+'
    CLASS_TESTS_URL = r'/professor/lesson/[0-9]+/test/'
    CLASS_ADD_TEST_URL = r'/professor/lesson/[0-9]+/test/add'
    CLASS_TESTS_BUTTON = (By.ID, "id_my_tests_button")
    CLASS_ADD_TEST_BUTTON = (By.ID, "id_add_test_button")
    CLASS_ADD_TEST_ONLINE_BUTTON = (By.ID, "id_add_test_online_button")
    MODIFY_TEST_BUTTON = (By.XPATH, "//a[@data-purpose='modify-test']")


class ClassPage(Browser):
    def navigate(self, base_url):
        pass

    def currently_on_this_page(self):
        return re.search(ClassPageLocator.URL, self.driver.current_url)

    def currently_on_class_tests_page(self):
        return re.search(ClassPageLocator.CLASS_TESTS_URL, self.driver.current_url)

    def currently_on_test_type_choice(self):
        return re.search(ClassPageLocator.CLASS_ADD_TEST_URL, self.driver.current_url)

    # Login page actions

    def access_class_tests(self):
        self.click_element(*ClassPageLocator.CLASS_TESTS_BUTTON)

    def add_new_test(self):
        self.click_element(*ClassPageLocator.CLASS_ADD_TEST_BUTTON)

    def add_online_test(self):
        self.click_element(*ClassPageLocator.CLASS_ADD_TEST_ONLINE_BUTTON)

    def modify_existing_test(self):
        self.click_element(*ClassPageLocator.MODIFY_TEST_BUTTON)
