import time

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from typing import List


class SeleniumBase:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.__wait = WebDriverWait(driver, 15, 0.3, ignored_exceptions=StaleElementReferenceException)
        self.driver.implicitly_wait(timeout)

    def __get_selenium_by(self, find_by: str) -> dict:
        '''Return a dictionary, where Keys are Strings representing a search locator strategies and Values are related By class values'''
        find_by = find_by.lower()
        locating = {'css': By.CSS_SELECTOR,
                    'xpath': By.XPATH,
                    'class_name': By.CLASS_NAME,
                    'id': By.ID,
                    'link_text': By.LINK_TEXT,
                    'name': By.NAME,
                    'partial_link_text': By.PARTIAL_LINK_TEXT,
                    'tag_name': By.TAG_NAME}
        return locating[find_by]

    def is_visible(self, find_by: str, locator: str, locator_name: str = None) -> WebElement:
        '''Waiting on element and return WebElement if it is visible'''
        return self.__wait.until(ec.visibility_of_element_located((self.__get_selenium_by(find_by), locator)), locator_name)

    def is_present(self, find_by: str, locator: str, locator_name: str = None) -> WebElement:
        '''Waiting on element and return WebElement if it is present on DOM'''
        return self.__wait.until(ec.presence_of_element_located((self.__get_selenium_by(find_by), locator)), locator_name)

    def is_not_present(self, find_by: str, locator: str, locator_name: str = None) -> WebElement:
        '''Wait on element until it disappears '''
        return self.__wait.until(ec.invisibility_of_element_located((self.__get_selenium_by(find_by), locator)),
                                 locator_name)

    def are_visible(self, find_by: str, locator: str, locator_name: str = None) -> List[WebElement]:
        '''Waiting on elements and return WebElements if they are visible'''
        return self.__wait.until(ec.visibility_of_all_elements_located((self.__get_selenium_by(find_by), locator)),
                                 locator_name)

    def are_present(self, find_by: str, locator: str, locator_name: str = None) -> List[WebElement]:
        '''Waiting on elements and return WebElements if they are present on DOM'''
        return self.__wait.until(ec.presence_of_all_elements_located((self.__get_selenium_by(find_by), locator)),
                                 locator_name)

    def get_text_from_webelements(self, elements: List[WebElement]) -> List[str]:
        '''The input should be a list of WebElements, where we read text from each element and Return a List[String]'''
        return [element.text for element in elements]

    def get_element_by_text(self, elements: List[WebElement], name: str) -> WebElement:
        '''The input should we a list of WebElements, from which we return a single WebElement found by it's name'''
        name = name.lower()
        return [element for element in elements if element.text.lower() == name][0]

    def delete_cookie(self, cookie_name: str) -> None:
        '''Delete a cookie by a name'''
        self.driver.delete_cookie(cookie_name)

    def scroll_down(self):
        '''Scroll down'''
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    def scroll_into_view(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def select_item_by_index(self, find_by: str, locator: str, locator_name: str = None, index: int = None):
        '''Select item by index from dropdown'''
        select = Select(self.is_present(find_by, locator, locator_name))
        select.select_by_index(index)

    def select_item_by_value(self, find_by: str, locator: str, locator_name: str = None, value: int = None):
        '''Select item by value from dropdown'''
        select = Select(self.is_present(find_by, locator, locator_name))
        select.select_by_value(value)

    def select_item_by_text(self, find_by: str, locator: str, locator_name: str = None, text: str = None):
        '''Select item by text from dropdown'''
        select = Select(self.is_present(find_by, locator, locator_name))
        select.select_by_visible_text(text)
