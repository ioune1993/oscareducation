from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from features import Browser


class CreateClassPageLocator(object):
    # Login page elements locator
    URL = 'professor/lesson/add/'
    CLASS_NAME_INPUT_ID = (By.ID, 'id_name')
    ClASS_STAGE_SELECT_ID = (By.ID, 'id_stage')
    SUBMIT = (By.XPATH, "//button[@type='submit']")


class CreateClassPage(Browser):
    def navigate(self, base_url):
        self.driver.get(base_url + CreateClassPageLocator.URL)

    def currently_on_this_page(self):
        return self.current_url_endswith(CreateClassPageLocator.URL)

    # Login page actions

    def click_element(self, *locator):
        self.driver.find_element(*locator).click()

    def enter_class_name(self, text):
        self.fill(text, *CreateClassPageLocator.CLASS_NAME_INPUT_ID)

    def select_id_stage(self, text):
        self.select(text, *CreateClassPageLocator.ClASS_STAGE_SELECT_ID)

    def submit(self):
        self.click_element(*CreateClassPageLocator.SUBMIT)