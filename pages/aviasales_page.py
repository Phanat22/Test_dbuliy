from selenium.webdriver.common.by import By

from base.seleniumbase import SeleniumBase
from pages.locators.aviasales_locators import AviasalesPageLocators


class AviasalesPage(SeleniumBase, AviasalesPageLocators):

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://phptravels.net/"

    def go_to_site(self):
        self.driver.get(self.url)

    def select_flight_trip(self):
        trip_block = self.is_visible('css', self.tabs_block, "Trip's tabs block is not present")
        trip_block.find_element(By.ID, self.flight_tab).click()

    def fill_flying_from_field(self, city_name):
        main_search_block = self.is_present('css', self.main_search_block, "Main search block block is not present")
        fly_from_field = main_search_block.find_element(By.ID, self.fly_from_field)
        fly_from_field.clear()
        fly_from_field.send_keys(city_name)
        self.are_present('css', self.dropdown_items, "Dropdown's items are not found")[0].click()

    def fill_destination_field(self, city_name):
        main_search_block = self.is_visible('css', self.main_search_block, "Main search block block is not present")
        destination_field = main_search_block.find_element(By.ID, self.destination_field)
        destination_field.clear()
        destination_field.send_keys(city_name)
        self.are_present('css', self.dropdown_items, "Dropdown's items are not found")[0].click()

    def select_departure_date(self, date):
        departure_date_field = self.is_visible('id', self.departure_date_field, "Departure field is not present")
        departure_date_field.clear()
        departure_date_field.send_keys(date)

    @property
    def search_btn(self):
        return self.is_visible('id', self.flights_search_btn, "Search button is not present")

    @property
    def tickets(self):
        return self.are_present('css', self.ticket_list, "Ticket list is not present")

    @property
    def price(self):
        ticket_block = self.is_present('css', self.ticket_block, "Price is not present")
        return ticket_block.find_elements(By.CSS_SELECTOR, self.price_fields)[0].text

    @property
    def book_btn(self):
        return self.are_present('css', self.book_now_btn, "Book button is not present")[0]

    @property
    def personal_block(self):
        return self.is_present('css', self.personal_info_block, "Personal info block is not present")

    def fill_first_name(self, name):
        self.personal_block.find_element(By.CSS_SELECTOR, self.first_name_field).send_keys(name)

    def fill_last_name(self, name):
        self.personal_block.find_element(By.CSS_SELECTOR, self.last_name_field).send_keys(name)

    def fill_email(self, email):
        self.personal_block.find_element(By.CSS_SELECTOR, self.email_field).send_keys(email)

    def fill_phone(self, phone):
        self.personal_block.find_element(By.CSS_SELECTOR, self.phone_field).send_keys(phone)

    def fill_address_field(self, address):
        self.personal_block.find_element(By.CSS_SELECTOR, self.address_field).send_keys(address)

    def select_country(self, country):
        self.personal_block.find_elements(By.CSS_SELECTOR, self.personal_info_ddwns)[0].click()
        self.is_present('css', self.search_country_field, "Personal info block is not present").send_keys(country)
        self.are_present('css', self.search_result_option, "Country options are not present")[0].click()

    def select_nationality(self, nationality):
        self.personal_block.find_elements(By.CSS_SELECTOR, self.personal_info_ddwns)[1].click()
        self.is_present('css', self.search_country_field, "Personal info block is not present").send_keys(nationality)
        self.are_present('css', self.search_result_option, "Country options are not present")[0].click()

    @property
    def adult_table(self):
        return self.is_present('css', self.adult_block, "Adult block is not present")

    def fill_adult_name(self, name):
        self.adult_table.find_element(By.CSS_SELECTOR, self.adult_first_name_field).send_keys(name)

    def fill_adult_last_name(self, name):
        self.adult_table.find_element(By.CSS_SELECTOR, self.adult_first_name_field).send_keys(name)

    def select_adult_nationality(self, nationality):
        self.adult_table.find_element(By.CSS_SELECTOR, self.nationality_ddwn).send_keys(nationality)

    def select_month(self, birth_day):
        self.adult_table.find_element(By.CSS_SELECTOR, self.month_ddwn).send_keys(birth_day)

    def select_day(self, day):
        self.adult_table.find_element(By.CSS_SELECTOR, self.day_ddwn).send_keys(day)

    def select_year(self, year):
        self.adult_table.find_element(By.CSS_SELECTOR, self.year_ddwn).send_keys(year)

    @property
    def select_agree_chbx(self):
        return self.is_present('css', self.agree_checkbox, "Agree chbx is not present")

    @property
    def confirm_booking_btn(self):
        return self.is_present('css', self.confirm_booking, "Confirm booking btn is not present")

    @property
    def invoice_tables(self):
        return self.are_present('css', self.invoice_tables_blocks, "Invoice tables are not present")

    @property
    def invoice_data(self):
        personal_data = self.invoice_tables[0].find_elements(By.CSS_SELECTOR, self.personal_data_items)
        return self.get_text_from_webelements(personal_data)

    @property
    def invoice_adult_data(self):
        personal_data = self.invoice_tables[1].find_elements(By.CSS_SELECTOR, self.personal_data_items)
        return self.get_text_from_webelements(personal_data)

    @property
    def invoice_price(self):
        return self.are_present('css', self.invoice_price_field, "Price is not present")
