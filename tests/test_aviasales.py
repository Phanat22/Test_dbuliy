from datetime import datetime

from pom.aviasales_page import AviasalesPage
from pom.class_assertion import Assertion


class TestAviasales:

    def test_book_ticket(self, setup):
        page = AviasalesPage(self.driver)
        page.go_to_site()

        page.select_flight_trip()
        fly_from_name = "Boryspil Intl"
        page.fill_flying_from_field(fly_from_name)

        destination_name = "Antalya"
        page.fill_destination_field(destination_name)

        departure_date = datetime.now().strftime("%d-%m-%Y")
        page.select_departure_date(departure_date)
        page.search_btn.click()

        assert len(page.tickets) != 0, "No tickets"
        price = page.price.strip('\nBook Now')
        page.book_btn.click()

        first_name = 'Automation'
        page.fill_first_name(first_name)

        last_name = 'test'
        page.fill_last_name(last_name)

        email_name = 'test@test.com'
        page.fill_email(email_name)

        phone = '+380673337733'
        page.fill_phone(phone)

        address = 'test'
        page.fill_address_field(address)

        country = 'Ukraine'
        page.select_country(country)

        nationality = 'Ukraine'
        page.select_nationality(nationality)

        adult_name = "Joy"
        page.fill_adult_name(adult_name)

        adult_last_name = 'Anderson'
        page.fill_adult_last_name(adult_last_name)

        nationality = 'Ukra'
        page.select_adult_nationality(nationality)

        month = '04'
        page.select_month(month)

        day = '6'
        page.select_day(day)

        year = '1990'
        page.select_year(year)

        _assert = Assertion()
        _assert.add(page.select_agree_chbx.is_selected() is False, "Checkbox was selected")
        page.scroll_down()
        page.select_agree_chbx.click()
        page.confirm_booking_btn.click()

        for data in page.invoice_data:
            if data == 'Email: info@travelagency.com' or data == 'Phone: +1-234-56789' or data == 'Address:':
                continue
            elif 'First Name' in data:
                _assert.add(first_name in data, f"Wrong name of passenger, exp=[{first_name}], act=[{data}]")
            elif 'Last Name' in data:
                _assert.add(last_name in data, f"Wrong last name of passenger, exp=[{last_name}], act=[{data}]")
            elif 'Email' in data:
                _assert.add(email_name in data, f"Wrong email, exp=[{email_name}], act=[{data}]")
            elif 'Phone' in data:
                _assert.add(phone in data, f"Wrong phone, exp=[{phone}], act=[{data}]")
            elif 'Address' in data:
                _assert.add(address in data, f"Wrong address, exp={address}, act={data}")

        for data in page.invoice_adult_data:
            if 'Guest 1' in data:
                _assert.add(adult_name+adult_last_name in data,
                            f"Wrong guest name, exp={adult_name+adult_last_name}, act={data}")
            elif 'Nationality' in data:
                _assert.add('UA' in data, f"Wrong nationality, exp=UA, act={data}")
            elif 'Date of Birth' in data:
                _assert.add(f'0{day}-{month}-{year}' in data, f"Wrong date of dirth,"
                                                              f" exp=0{day}-{month}-{year}, act={data}")

        _assert.add(page.invoice_price[-1].text.lstrip('Total Price: ') == price,
                    f"Wrong price in invoice, exp={price}, act={page.invoice_price[-1].text.lstrip('Total Price: ')}")
        _assert.do_assert()
