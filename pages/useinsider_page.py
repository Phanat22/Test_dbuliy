import time

from selenium.webdriver.common.by import By
from base.seleniumbase import SeleniumBase

from pages.locators.useinsider_locators import UseinsiderPageLocators
from pages.class_assertion import Assertion


class UseinsiderPage(SeleniumBase, UseinsiderPageLocators):

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://useinsider.com/"

    def go_to_site(self):
        self.driver.get(self.url)

    def select_accept_all_cookies(self):
        self.is_visible('css', self.accept_all_btn, "Accept btn is not present").click()
        self.is_not_present('css', self.accept_all_btn, "Accept btn is present, but should not be present")

    def get_nav_bar_items(self):
        self.is_visible('css', self.navigation_bar_block, "Navigation block is not visible")
        return self.are_present('css', self.nav_bar_items, 'Header Navigation items are not visible')

    def select_nav_bar_item(self, name):
        nav_links = self.get_nav_bar_items()
        nav_links_text = self.get_text_from_webelements(nav_links)
        assert name in nav_links_text, f"{name} is missing in {nav_links_text}"
        name_index = nav_links_text.index(name)
        nav_links[name_index].click()

    def select_more_block(self, name):
        self.is_visible('css', self.more_menu_general_block, "More block is not visible")
        more_items = self.are_visible('css', self.more_menu_block_items, "Items into More block ate not found")
        more_items_text = self.get_text_from_webelements(more_items)
        exp_text = list()
        for i in more_items_text:
            if name in i:
                exp_text.append(i)
        item_index = more_items_text.index(exp_text[0])
        more_items[item_index].click()

    def check_team_block_is_present(self):
        team_block = self.is_present('css', self.team_block, "team block is not present")
        return team_block

    def scroll_and_see_all_teams(self):
        team_block = self.check_team_block_is_present()
        teams_btn = team_block.find_element(By.CSS_SELECTOR, self.see_all_teams_btn)
        team_items_block = team_block.find_elements(By.CSS_SELECTOR, self.team_block_items_block)[0]
        self.scroll_into_view(team_items_block)
        self.driver.execute_script("arguments[0].click();", teams_btn)
        time.sleep(2)

    def check_locations_block_is_present(self):
        return self.is_present('css', self.location_block, "location block is not present")

    def check_life_at_insider_block_is_present(self):
        return self.is_present('css', self.life_at_insider_block, "life at insider block is not present")

    def select_team_item(self, name):
        team_block = self.check_team_block_is_present()
        teams_items = team_block.find_elements(By.CSS_SELECTOR, self.team_block_items)
        exp_item = list()
        for i in teams_items:
            if name in i.text:
                exp_item.append(i)
        self.scroll_into_view(exp_item[0])
        item_href = exp_item[0].find_element(By.CSS_SELECTOR, self.team_href)
        self.driver.get(item_href.get_attribute('href'))

    def see_all_jobs_btn_click(self):
        job_btn = self.is_present('css', self.see_all_jobs_button, "See all jobs btn is not present")
        get_href = job_btn.find_element(By.CSS_SELECTOR, 'a')
        self.driver.get(get_href.get_attribute('href'))
        time.sleep(2)

    def select_item_from_location_ddwn(self, location):
        time.sleep(2)
        location_dd = self.is_present('css', self.location_dropdown, "Location dropdown is not present")
        location_dd.click()
        self.is_present('css', self.location_dd_results, "Location dropdown not expanding")
        results_items = self.are_present('css', self.location_dd_items, "Items are not present")
        items_text = self.get_text_from_webelements(results_items)
        location_index = items_text.index(location)
        results_items[location_index].click()
        assert location_dd.get_attribute('title') == location, "Wrong selected location"

    def select_item_from_department_ddwn(self, location):
        department_dd = self.is_present('css', self.department_dropdown, "Department dropdown is not present")
        department_dd.click()
        self.is_present('css', self.department_dd_results, "Department dropdown not expanding")
        results_items = self.are_present('css', self.department_dd_items, "Items are not present")
        items_text = self.get_text_from_webelements(results_items)
        department_index = items_text.index(location)
        results_items[department_index].click()
        assert department_dd.get_attribute('title') == location, "Wrong selected department"

    def check_selected_position(self, position, department, location, btn_link):
        job_list_block = self.is_present('css', self.jod_list_block, "Job list is not present")
        self.scroll_into_view(job_list_block)
        time.sleep(2)
        job_positions = self.are_present('css', self.jod_items, "Job items are missing")
        _assert = Assertion()
        for pos in job_positions:
            pos_name = pos.find_element(By.CSS_SELECTOR, self.job_position_name)
            department_name = pos.find_element(By.CSS_SELECTOR, self.job_department_name)
            location_name = pos.find_element(By.CSS_SELECTOR, self.job_location_name)
            job_apply_bnt = pos.find_element(By.CSS_SELECTOR, self.job_apply_bnt)

            _assert.add(position in pos_name.text, "Wrong name of position")\
                .add(department == department_name.text, "Wrong name of department")\
                .add(location in location_name.text, "Wrong name of location")\
                .add(btn_link in job_apply_bnt.get_attribute('href'), "Wrong link of apply button")\
                .do_assert()

    def apply_position_and_check_switch(self, url, pos_name):
        job_positions = self.are_present('css', self.jod_items, "Job items are missing")
        job_apply_bnt = job_positions[0].find_element(By.CSS_SELECTOR, self.job_apply_bnt)
        self.driver.get(job_apply_bnt.get_attribute('href'))
        time.sleep(2)

        url_page = self.driver.current_url
        title = self.is_present('css', self.lever_position_name_title, "Title of position is not present")
        title_text = title.find_element(By.CSS_SELECTOR, 'h2')

        _assert = Assertion()
        _assert\
            .add(url in url_page, "Wrong url of page")\
            .add(pos_name in title_text.text, "Wrong text of title")\
            .do_assert()
