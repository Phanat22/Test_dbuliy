from pages.useinsider_page import UseinsiderPage

MORE_DATA = "More"
CAREERS_DATA = "Careers"
POSITION_DATA = "Quality Assurance"
CITY_DATA = "Istanbul, Turkey"
NAV_BAR_ITEMS = 'Platform,Industries,Use Cases,Resources,Blog,More,Product Demo Hub,'
JOBS_LEVER_LINK = 'https://jobs.lever.co/useinsider'


class TestUseinsider:

    def test_useinsider(self):
        page = UseinsiderPage(self.driver)
        page.go_to_site()
        page.select_accept_all_cookies()
        page.get_nav_bar_items()
        assert page.get_nav_bar_items_text() == NAV_BAR_ITEMS, "Wrong items of navigation bar menu"
        page.select_nav_bar_item(MORE_DATA)
        page.select_more_block(CAREERS_DATA)
        page.check_team_block_is_present()
        page.check_locations_block_is_present()
        page.check_life_at_insider_block_is_present()
        page.scroll_and_see_all_teams()
        page.select_team_item(POSITION_DATA)
        page.see_all_jobs_btn_click()
        page.select_item_from_location_ddwn(CITY_DATA)
        page.select_item_from_department_ddwn(POSITION_DATA)
        page.check_selected_position(POSITION_DATA, POSITION_DATA, CITY_DATA, JOBS_LEVER_LINK)
        page.apply_position_and_check_switch(JOBS_LEVER_LINK, POSITION_DATA)
