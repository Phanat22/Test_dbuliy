## Set up

1. Install pytest
2. Install selenium library
3. Install selenium webdriver, chromedriver, geckodriver

## Run tests

 * pytest -v tests/test_homepage.py
 * pytest -v tests/test_homepage.py -k test_nav_links
 * pytest -v tests/test_aviasales.py
 * pytest -v  tests/test_pet.py 
 * pytest -v --browser_name=chrome tests/test_useinsider.py
 * pytest -v --browser_name=firefox tests/test_useinsider.py
