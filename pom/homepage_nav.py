from typing import List
from selenium.webdriver.remote.webelement import WebElement

from base.seleniumbase import SeleniumBase


class HomepageNav(SeleniumBase):

    def __init__(self, driver):
        super().__init__(driver)
        self.url = 'https://www.macys.com/'
        self.sign_in_btn = 'myRewardsLabel'
        self.sign_in_block = 'sign-in-section'
        self.__nav_links = '#mainNavigationFobs>li'

    def go_to_site(self):
        return self.driver.get(self.url)

    def get_sign_in_btn(self):
        return self.is_visible('id', self.sign_in_btn, 'Sign in button')

    def check_sign_in_form_is_present(self):
        return self.is_visible('id', self.sign_in_block, 'Sign in block')

    def get_nav_links(self) -> List[WebElement]:
        '''Return WebElements for nav links'''
        return self.are_visible('css', self.__nav_links, 'Header Navigation Links')

    def get_nav_links_text(self) -> str:
        '''Return all nav links text. Return format is a String with comma separated values'''
        nav_links = self.get_nav_links()
        nav_links_text = self.get_text_from_webelements(nav_links)
        return ','.join(nav_links_text)

    def get_nav_link_by_name(self, name: str) -> WebElement:
        '''Return a nav link WebElement, the input is a link's name'''
        elements = self.get_nav_links()
        return self.get_element_by_text(elements, name)
