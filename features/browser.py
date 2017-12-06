"""
Browser configuration for the Behaviour-Driven-Development environment
"""
import abc
import codecs
import os
from selenium import webdriver
from datetime import datetime

from selenium.webdriver.support.select import Select


class Browser(object):
    # PhantomJS is used there (headless browser - meaning we can execute tests in a command-line environment,
    # which is what we want for use with SemaphoreCI
    # For debugging purposes, you can use the Firefox driver instead.
    driver = webdriver.PhantomJS()
    # Small unit of wait between instructions, allowing things to load
    driver.implicitly_wait(30)
    # Screen size must be wide enough to let PhantomJS find elements
    driver.set_window_size(1920, 1080)

    def quit(self):
        self.driver.quit()

    def current_url(self):
        return self.driver.current_url

    def save_screen_shot(self, context, step):
        # Screenshots where that step failed
        self.driver.save_screenshot('features/failures/screenshots/' + str(datetime.now()) + '-' + step.name + '.png')
        save_path = 'features/failures/pages'
        file_name = str(datetime.now()) + '-' + str(step.name) + '.html'
        complete_name = os.path.join(save_path, file_name)
        file_object = codecs.open(complete_name, "w", "utf-8")
        html = context.browser.driver.page_source
        file_object.write(html)

    def current_url_endswith(self, url):
        return self.driver.current_url.endswith(url)

    # Pages methods

    def fill(self, text, *locator):
        self.driver.find_element(*locator).clear()
        self.driver.find_element(*locator).send_keys(text)

    def click_element(self, *locator):
        self.driver.find_element(*locator).click()

    def select(self, text, *locator):
        Select(self.driver.find_element(*locator)).select_by_value(text)

    @abc.abstractmethod
    def navigate(self, base_url):
        pass
