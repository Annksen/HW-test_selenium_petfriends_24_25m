from selenium.webdriver.common.by import By
import time


def test_search_example(selenium):

    selenium.get('https://www.google.com')

    time.sleep(5)

    search_input = selenium.find_element(By.ID, 'APjFqb')

    search_input.clear()
    search_input.send_keys('my first selenium test for Web UI!')

    time.sleep(5)

    search_button = selenium.find_element(By.NAME, 'btnK')
    search_button.submit()

    time.sleep(10)

    selenium.save_screenshot('result.png')
