import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from features import Browser


class AddOnlineTestPageLocator(object):
    # Login page elements locator
    URL = r'/professor/lesson/[0-9]+/test/online/add'
    SKILL_SELECTOR = (By.XPATH, "//select[@ng-model='stage13SelectedSkill']")
    ADD_SKILL_BUTTON = (By.ID, "addSkillToTestButtonForStage13")
    CREATE_TEST_BUTTON = (By.ID, "id_create_test_button")
    TEST_NAME_INPUT = (By.ID, "test_name")


class AddOnlineTestPage(Browser):
    def navigate(self, base_url):
        pass

    def currently_on_this_page(self):
        return re.search(AddOnlineTestPageLocator.URL, self.driver.current_url)

    # Login page actions

    def select_skill(self, skill):
        self.select(skill, *AddOnlineTestPageLocator.SKILL_SELECTOR)

    def add_skill(self):
        self.click_element(*AddOnlineTestPageLocator.ADD_SKILL_BUTTON)

    def create_test(self):
        self.click_element(*AddOnlineTestPageLocator.CREATE_TEST_BUTTON)

    def add_test_name(self, name):
        self.fill(name, *AddOnlineTestPageLocator.TEST_NAME_INPUT)

