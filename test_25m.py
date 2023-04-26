import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import webdriver
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.WebDriver('/Users/Nusha/PycharmProjects/python1151/python115/24m/chromedriver')
    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends.skillfactory.ru/login')

    yield

    pytest.driver.quit()


def test_show_my_pets():
    # Вводим email
    pytest.driver.find_element(By.ID, 'email').send_keys('n@ya.ru')
    # Вводим пароль
    pytest.driver.find_element(By.ID, 'pass').send_keys('1234')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    time.sleep(5)
    assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    pytest.driver.find_element(By.CSS_SELECTOR, 'div#navbarNav>ul>li>a').click()
    assert pytest.driver.find_element(By.TAG_NAME, 'h2').text == "Ann78"


    pytest.driver.implicitly_wait(5)
    images = pytest.driver.find_elements(By.CSS_SELECTOR, 'div#all_my_pets>table>tbody>tr>th>img')
    pytest.driver.implicitly_wait(5)
    names = pytest.driver.find_elements(By.XPATH, '//tr/th/following-sibling::td[1]')
    pytest.driver.implicitly_wait(5)
    types = pytest.driver.find_elements(By.XPATH, '//tr/th/following-sibling::td[2]')
    pytest.driver.implicitly_wait(5)
    ages = pytest.driver.find_elements(By.XPATH, '//tr/th/following-sibling::td[3]')

    # Общее количество питомцев пользователя из статистики
    user_stat_element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "html>body>div>div>div")))
    user_pets_count = int(user_stat_element.text.split("\n")[1].split(":")[1].strip())

    # тест1: Присутствуют все питомцы.
    assert user_pets_count == len(names)

    pets_with_foto_count: int = 0
    pets_names = []
    pets_types = []
    pets_ages = []

    for i in range(len(names)):
        if images[i].get_attribute('src') != '':
            pets_with_foto_count += 1

            # тест3: У всех питомцев есть имя, возраст и порода
            assert names[i].text != ''
            assert types[i].text != ''
            assert ages[i].text != ''

            if names[i].text != '':
                pets_names.append(names[i].text)

            if types[i].text != '':
                pets_types.append(types[i].text)

            if ages[i].text != '':
                pets_ages.append(ages[i].text)

            # тест2: Хотя бы у половины питомцев есть фото.
        assert pets_with_foto_count >= user_pets_count / 2

        # тест4: У всех питомцев разные имена.
        assert len(pets_names) == len(set(pets_names))

        # тест5: В списке нет повторяющихся питомцев.
        assert len(set(pets_names)) == user_pets_count or len(set(pets_types)) == user_pets_count or len(
            set(pets_ages)) == user_pets_count


    # images = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
    # names = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
    # descriptions = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')
    #
    # for i in range(len(names)):
    #     assert images[i].get_attribute('src') != ''
    #     assert names[i].text != ''
    #     assert descriptions[i].text != ''
    #     assert ', ' in descriptions[i]
    #     parts = descriptions[i].text.split(", ")
    #     assert len(parts[0]) > 0
    #     assert len(parts[1]) > 0



