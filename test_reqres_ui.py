import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


@pytest.fixture(scope="module")
def browser():
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get("https://reqres.in/")
    yield driver
    driver.quit()


class TestReqRes:
    # Тест на проверку наличия элемента users на странице
    def test_users_link(self, browser):
        users_link = browser.find_element(By.CLASS_NAME, 'active')
        assert users_link.is_displayed()

    # Тест на проверку наличия элемента users-single на странице
    def test_users_single(self, browser):
        users_single = browser.find_element(By.CSS_SELECTOR, '[data-id="users-single"]')
        assert users_single.is_displayed()

    # Тест на проверку наличия элемента users-single-not-found на странице
    def test_users_single_not_found(self, browser):
        users_single_not_found = browser.find_element(By.CSS_SELECTOR, '[data-id="users-single-not-found"]')
        assert users_single_not_found.is_displayed()

    # Тест на проверку наличия элемента unknown на странице
    def test_unknown(self, browser):
        unknown = browser.find_element(By.CSS_SELECTOR, '[data-id="unknown"]')
        assert unknown.is_displayed()

    # Тест на проверку наличия элемента unknown-single на странице
    def test_unknown_single(self, browser):
        unknown_single = browser.find_element(By.CSS_SELECTOR, '[data-id="unknown-single"]')
        assert unknown_single.is_displayed()

    # Тест на проверку наличия элемента unknown-single-not-found на странице
    def test_unknown_single_not_found(self, browser):
        unknown_single_not_found = browser.find_element(By.CSS_SELECTOR, '[data-id="unknown-single-not-found"]')
        assert unknown_single_not_found.is_displayed()

    # Тест на проверку наличия элемента post на странице
    def test_post(self, browser):
        post = browser.find_element(By.CSS_SELECTOR, '[data-id="post"]')
        assert post.is_displayed()

    # Тест на проверку наличия элемента put на странице
    def test_put(self, browser):
        put = browser.find_element(By.CSS_SELECTOR, '[data-id="put"]')
        assert put.is_displayed()

    # Тест на проверку наличия элемента patch на странице
    def test_patch(self, browser):
        patch = browser.find_element(By.CSS_SELECTOR, '[data-id="patch"]')
        assert patch.is_displayed()

    # Тест на проверку наличия элемента delete на странице
    def test_delete(self, browser):
        delete = browser.find_element(By.CSS_SELECTOR, '[data-id="delete"]')
        assert delete.is_displayed()

    # Тест на проверку наличия элемента register-successful на странице
    def test_register_successful(self, browser):
        register_successful = browser.find_element(By.CSS_SELECTOR, '[data-id="register-successful"]')
        assert register_successful.is_displayed()

    # Тест на проверку наличия элемента register-unsuccessful на странице
    def test_register_unsuccessful(self, browser):
        register_unsuccessful = browser.find_element(By.CSS_SELECTOR, '[data-id="register-unsuccessful"]')
        assert register_unsuccessful.is_displayed()

    # Тест на проверку наличия элемента login-successful на странице
    def test_login_successful(self, browser):
        login_successful = browser.find_element(By.CSS_SELECTOR, '[data-id="login-successful"]')
        assert login_successful.is_displayed()

    # Тест на проверку наличия элемента login-unsuccessful на страниц
    def test_login_unsuccessful(self, browser):
        login_unsuccessful = browser.find_element(By.CSS_SELECTOR, '[data-id="login-unsuccessful"]')
        assert login_unsuccessful.is_displayed()

    # Тест на дилей
    def test_delay(self, browser):
        delay = browser.find_element(By.CSS_SELECTOR, '[data-id="delay"]')
        assert delay.is_displayed()
