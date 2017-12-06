from selenium.webdriver.common.by import By
from features import Browser


class TestModifyPageLocator(object):
    # Login page elements locator
    QUESTION_GENERATOR_BUTTON = (By.ID, "id_generate_button")


class TestModifyPage(Browser):
    def navigate(self, base_url):
        pass
    # Login page actions

    def click_on_generate_questions(self):
        self.click_element(*TestModifyPageLocator.QUESTION_GENERATOR_BUTTON)
