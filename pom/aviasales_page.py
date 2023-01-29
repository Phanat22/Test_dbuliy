from selenium.webdriver.common.by import By

from base.seleniumbase import SeleniumBase


class AviasalesPage(SeleniumBase):

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://phptravels.net/"
        self.__tabs_block = "[id='Tab']"
        self.__flight_tab = "flights-tab"
        self.__search_desc_block = "TabContent"
        self.__fly_from_field = "autocomplete"
        self.__destination_field = "autocomplete2"
        self.__main_search_block = "[class='main_search']"
        self.__dropdown_items = '[class="autocomplete-result"]'
        self.__departure_date_field = 'departure'
        self.__flights_search_btn = 'flights-search'
        self.__ticket_list = '[class="theme-search-results-item-mask-link"]'
        self.__book_now_btn = '[class="btn btn-primary"]'
        self.__ticket_block = '[class="row g-3"]'
        self.__price_fields = '[class*="ladda waves-effect"]'
        self.__personal_info_block = '[class="form-box mb-2"]'
        self.__first_name_field = '[name="firstname"]'
        self.__last_name_field = '[name="lastname"]'
        self.__email_field = '[name="email"]'
        self.__phone_field = '[name="phone"]'
        self.__personal_info_ddwns = '[class="select2-selection select2-selection--single"]'
        self.__address_field = '[name="address"]'
        self.__search_country_field = '[type="search"]'
        self.__search_result_option = '[class="select2-results"]>ul>li'
        self.__adult_block = '[class="card mb-3"]'
        self.__adult_first_name_field = '[name="firstname_1"]'
        self.__adult_last_name_field = '[name="lastname_1"]'
        self.__nationality_ddwn = '[name="nationality_1"]'
        self.__month_ddwn = '[name="dob_month_1"]'
        self.__day_ddwn = '[name="dob_day_1"]'
        self.__year_ddwn = '[name="dob_year_1"]'
        self.__agree_checkbox = '[class="custom-checkbox"]'
        self.__confirm_booking = '[id="booking"]'
        self.__invoice_tables_blocks = '[class="card-body"]'
        self.__personal_data_items = '[class="customer"]>li'
        self.__invoice_price_field = '[class="list-group-item"]'

    def go_to_site(self):
        self.driver.get(self.url)
        self.driver.implicitly_wait(5)

    def select_flight_trip(self):
        trip_block = self.is_visible('css', self.__tabs_block, "Trip's tabs block is not present")
        trip_block.find_element(By.ID, self.__flight_tab).click()

    def fill_flying_from_field(self, city_name):
        main_search_block = self.is_present('css', self.__main_search_block, "Main search block block is not present")
        fly_from_field = main_search_block.find_element(By.ID, self.__fly_from_field)
        fly_from_field.clear()
        fly_from_field.send_keys(city_name)
        self.are_present('css', self.__dropdown_items, "Dropdown's items are not found")[0].click()

    def fill_destination_field(self, city_name):
        main_search_block = self.is_visible('css', self.__main_search_block, "Main search block block is not present")
        destination_field = main_search_block.find_element(By.ID, self.__destination_field)
        destination_field.clear()
        destination_field.send_keys(city_name)
        self.are_present('css', self.__dropdown_items, "Dropdown's items are not found")[0].click()

    def select_departure_date(self, date):
        departure_date_field = self.is_visible('id', self.__departure_date_field, "Departure field is not present")
        departure_date_field.clear()
        departure_date_field.send_keys(date)

    @property
    def search_btn(self):
        return self.is_visible('id', self.__flights_search_btn, "Search button is not present")

    @property
    def tickets(self):
        return self.are_present('css', self.__ticket_list, "Ticket list is not present")

    @property
    def price(self):
        ticket_block = self.is_present('css', self.__ticket_block, "Price is not present")
        return ticket_block.find_elements(By.CSS_SELECTOR, self.__price_fields)[0].text

    @property
    def book_btn(self):
        return self.are_present('css', self.__book_now_btn, "Book button is not present")[0]

    @property
    def personal_block(self):
        return self.is_present('css', self.__personal_info_block, "Personal info block is not present")

    def fill_first_name(self, name):
        self.personal_block.find_element(By.CSS_SELECTOR, self.__first_name_field).send_keys(name)

    def fill_last_name(self, name):
        self.personal_block.find_element(By.CSS_SELECTOR, self.__last_name_field).send_keys(name)

    def fill_email(self, email):
        self.personal_block.find_element(By.CSS_SELECTOR, self.__email_field).send_keys(email)

    def fill_phone(self, phone):
        self.personal_block.find_element(By.CSS_SELECTOR, self.__phone_field).send_keys(phone)

    def fill_address_field(self, address):
        self.personal_block.find_element(By.CSS_SELECTOR, self.__address_field).send_keys(address)

    def select_country(self, country):
        self.personal_block.find_elements(By.CSS_SELECTOR, self.__personal_info_ddwns)[0].click()
        self.is_present('css', self.__search_country_field, "Personal info block is not present").send_keys(country)
        self.are_present('css', self.__search_result_option, "Country options are not present")[0].click()

    def select_nationality(self, nationality):
        self.personal_block.find_elements(By.CSS_SELECTOR, self.__personal_info_ddwns)[1].click()
        self.is_present('css', self.__search_country_field, "Personal info block is not present").send_keys(nationality)
        self.are_present('css', self.__search_result_option, "Country options are not present")[0].click()

    @property
    def adult_table(self):
        return self.is_present('css', self.__adult_block, "Adult block is not present")

    def fill_adult_name(self, name):
        self.adult_table.find_element(By.CSS_SELECTOR, self.__adult_first_name_field).send_keys(name)

    def fill_adult_last_name(self, name):
        self.adult_table.find_element(By.CSS_SELECTOR, self.__adult_first_name_field).send_keys(name)

    def select_adult_nationality(self, nationality):
        self.adult_table.find_element(By.CSS_SELECTOR, self.__nationality_ddwn).send_keys(nationality)

    def select_month(self, birth_day):
        self.adult_table.find_element(By.CSS_SELECTOR, self.__month_ddwn).send_keys(birth_day)

    def select_day(self, day):
        self.adult_table.find_element(By.CSS_SELECTOR, self.__day_ddwn).send_keys(day)

    def select_year(self, year):
        self.adult_table.find_element(By.CSS_SELECTOR, self.__year_ddwn).send_keys(year)

    @property
    def select_agree_chbx(self):
        return self.is_present('css', self.__agree_checkbox, "Agree chbx is not present")

    @property
    def confirm_booking_btn(self):
        return self.is_present('css', self.__confirm_booking, "Confirm booking btn is not present")

    @property
    def invoice_tables(self):
        return self.are_present('css', self.__invoice_tables_blocks, "Invoice tables are not present")

    @property
    def invoice_data(self):
        personal_data = self.invoice_tables[0].find_elements(By.CSS_SELECTOR, self.__personal_data_items)
        return self.get_text_from_webelements(personal_data)

    @property
    def invoice_adult_data(self):
        personal_data = self.invoice_tables[1].find_elements(By.CSS_SELECTOR, self.__personal_data_items)
        return self.get_text_from_webelements(personal_data)

    @property
    def invoice_price(self):
        return self.are_present('css', self.__invoice_price_field, "Price is not present")
