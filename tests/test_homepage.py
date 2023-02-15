import pytest

from pages.homepage_nav import HomepageNav

NAV_LINK_TEXT = 'Women,Men,Kids,Home,Beauty,Shoes,Handbags,Jewelry,Furniture,Toys,Gifts,Trending,Sale'


class TestHomepage:

    @pytest.fixture(autouse=True)
    def get_url(self):
        self.page = self.__class__.page = HomepageNav(self.driver)
        self.page.go_to_site()

    @pytest.mark.smoke
    def test_nav_links(self):
        assert self.page.get_nav_links_text() == NAV_LINK_TEXT, 'Wrong tab names'

    @pytest.mark.smoke
    def test_check_go_to_sign_in_form(self):
        self.page.get_sign_in_btn().click()
        self.page.check_sign_in_form_is_present()
