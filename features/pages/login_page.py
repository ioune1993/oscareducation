from selenium.webdriver.common.by import By
from features import Browser


class LoginPageLocator(object):
    # Login page elements locator
    USERNAME_INPUT = (By.ID, 'id_username')
    PASSWORD_INPUT = (By.ID, 'id_password')
    SUBMIT = (By.XPATH, "//input[@type='submit']")
    USERNAME_LOGIN_URL = '/accounts/usernamelogin/'
    PASSWORD_LOGIN_URL = '/accounts/passwordlogin/'
    ALERT = 'alert-danger'


class LoginPage(Browser):
    # Login page actions

    def navigate(self, base_url):
        self.driver.get(base_url + LoginPageLocator.USERNAME_LOGIN_URL)

    def enter_username(self, text):
        self.fill(text, *LoginPageLocator.USERNAME_INPUT)

    def enter_password(self, text):
        self.fill(text, *LoginPageLocator.PASSWORD_INPUT)

    def submit(self):
        self.click_element(*LoginPageLocator.SUBMIT)

    def find_alert(self):
        return self.driver.find_element_by_class_name(LoginPageLocator.ALERT)

    def currently_on_password_page(self):
        return self.current_url_endswith(LoginPageLocator.PASSWORD_LOGIN_URL)

    def currently_on_username_page(self):
        return self.current_url_endswith(LoginPageLocator.USERNAME_LOGIN_URL)
