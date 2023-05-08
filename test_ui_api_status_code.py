import requests
import json
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time


@pytest.fixture(scope="module")
def browser():
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get("https://reqres.in/")
    yield driver
    driver.quit()


# Сравнение статус кодов и JSON ответа API и UI, всех методов которые представлены на странице https://reqres.in/
class TestApiUi:
    @pytest.mark.parametrize("api_url, css_selector, method", [
        ('https://reqres.in/api/users?page=2', '[data-id="users"]', 'GET'),
        ('https://reqres.in/api/users/2', '[data-id="users-single"]', 'GET'),
        ('https://reqres.in/api/users/23', '[data-id="users-single-not-found"]', 'GET'),
        ('https://reqres.in/api/unknown', '[data-id="unknown"]', 'GET'),
        ('https://reqres.in/api/unknown/2', '[data-id="unknown-single"]', 'GET'),
        ('https://reqres.in/api/unknown/23', '[data-id="unknown-single-not-found"]', 'GET'),
        ('https://reqres.in/api/users?delay=3', '[data-id="delay"]', 'GET'),
        ('https://reqres.in/api/users', '[data-id="post"]', 'POST'),
        ('https://reqres.in/api/users/2', '[data-id="put"]', 'PUT'),
        ('https://reqres.in/api/users/2', '[data-id="patch"]', 'PATCH'),
        ('https://reqres.in/api/users/2', '[data-id="delete"]', 'DELETE'),
        ('https://reqres.in/api/register', '[data-id="register-successful"]', 'POST'),
        ('https://reqres.in/api/register', '[data-id="register-unsuccessful"]', 'POST'),
        ('https://reqres.in/api/login', '[data-id="login-successful"]', 'POST'),
        ('https://reqres.in/api/login', '[data-id="login-unsuccessful"]', 'POST')
    ])
    def test_api_ui_params(self, api_url, css_selector, browser, method):
        browser.find_element(By.CSS_SELECTOR, css_selector).click()
        time.sleep(4)
        ui_response = browser.find_element(By.CSS_SELECTOR, '[data-key="output-response"]').text
        ui_response_status_code = browser.find_element(By.CSS_SELECTOR, '[data-key="response-code"]').text
        if method == 'GET':
            api_response = requests.get(api_url).json()
            api_response_status_code = requests.get(api_url)
            api_status_code = api_response_status_code.status_code
            assert api_status_code == int(ui_response_status_code)
            assert api_response == json.loads(ui_response)
        elif method == 'POST' and api_url == 'https://reqres.in/api/users':
            # сравнение в методе POST происходит только на консистентность полей "name" и "job", тк поля createdAt и Id будут уникальными.
            payload = {'name': 'morpheus', 'job': 'leader'}
            api_response = requests.post(api_url, json=payload).json()
            api_status_code = requests.post(api_url, json=payload).status_code
            assert api_status_code == int(ui_response_status_code)
            assert api_response['name'] == json.loads(ui_response)['name']
            assert api_response['job'] == json.loads(ui_response)['job']
        elif method == 'PUT' and api_url == 'https://reqres.in/api/users/2':
            # сравнение в методе PUT происходит только на консистентность полей "name" и "job", тк поля createdAt и Id будут уникальными.
            payload = {'name': 'morpheus', 'job': 'zion resident'}
            api_response = requests.put(api_url, json=payload).json()
            api_status_code = requests.put(api_url, json=payload).status_code
            assert api_status_code == int(ui_response_status_code)
            assert api_response['name'] == json.loads(ui_response)['name']
            assert api_response['job'] == json.loads(ui_response)['job']
        elif method == 'PATCH' and api_url == 'https://reqres.in/api/users/2':
            # сравнение в методе PATCH происходит только на консистентность полей "name" и "job", тк поля createdAt и Id будут уникальными.
            payload = {'name': 'morpheus', 'job': 'zion resident'}
            api_response = requests.patch(api_url, json=payload).json()
            api_status_code = requests.patch(api_url, json=payload).status_code
            assert api_status_code == int(ui_response_status_code)
            assert api_response['name'] == json.loads(ui_response)['name']
            assert api_response['job'] == json.loads(ui_response)['job']
        elif method == 'DELETE' and api_url == 'https://reqres.in/api/users/2':
            # сравнение в методе DELE происходит только на консистентность полей "name" и "job", тк поля createdAt и Id будут уникальными.
            payload = {'name': 'morpheus', 'job': 'zion resident'}
            api_status_code = requests.delete(api_url, json=payload).status_code
            assert api_status_code == int(ui_response_status_code)
        elif css_selector == '[data-id="register-successful"]':
            # Позитивный POST регистрация
            payload = {'email': 'eve.holt@reqres.in', 'password': 'pistol'}
            api_response = requests.post(api_url, json=payload).json()
            api_status_code = requests.post(api_url, json=payload).status_code
            assert api_status_code == int(ui_response_status_code)
            assert api_response == json.loads(ui_response)
        elif css_selector == '[data-id="register-unsuccessful"]':
            # Негавный POST регистрация
            payload = {'email': "sydney@fife"}
            response = requests.post(api_url, json=payload)
            api_response = response.json()
            api_status_code = response.status_code
            assert api_status_code == int(ui_response_status_code)
            assert api_response == json.loads(ui_response)
        elif css_selector == '[data-id="login-successful"]':
            # позитивный POST логин
            payload = {'email': "eve.holt@reqres.in", 'password': "cityslicka"}
            response = requests.post(api_url, json=payload)
            api_response = response.json()
            api_status_code = response.status_code
            assert api_status_code == int(ui_response_status_code)
            assert api_response == json.loads(ui_response)
        elif css_selector == '[data-id="login-unsuccessful"]':
            # Негавный POST логин
            payload = {'email': "peter@klaven"}
            response = requests.post(api_url, json=payload)
            api_response = response.json()
            api_status_code = response.status_code
            assert api_status_code == int(ui_response_status_code)
            assert api_response == json.loads(ui_response)




