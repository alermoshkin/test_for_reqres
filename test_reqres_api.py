import requests
import pytest
from test_params import *


# Позитивные тесты для получения списка пользователей с разными параметрами page
@pytest.mark.parametrize('page', params_page)
def test_get_users(page):
    response = requests.get(f'https://reqres.in/api/users?page={page}')
    assert response.status_code == 200
    assert len(response.json()['data']) > 0

# Негативные тесты для получения списка пользователей с некорректными параметрами page
@pytest.mark.parametrize('page', params_page_negative)
def test_get_users_negative(page):
    response = requests.get(f'https://reqres.in/api/users?page={page}')
    assert response.status_code >= 400

# Позитивные тесты на получение одного пользователя
@pytest.mark.parametrize('id', params_user_id)
def test_get_single_user(id):
    response = requests.get(f'https://reqres.in/api/users/{id}')
    assert response.status_code == 200
    assert 'data' in response.json().keys()

# Негативный тест на получение одного пользователя с неккоректным id
def test_get_single_users_negative():
    response = requests.get('https://reqres.in/api/users/negative')
    assert response.status_code >= 400

# Позитивный тест поиска несуществующего пользователя
def test_get_single_user_not_found():
    response = requests.get('https://reqres.in/api/users/9999')
    assert response.status_code == 404

# Позитивные тесты вывода списка ресурсов
@pytest.mark.parametrize("page, per_page", params_resource)
def test_get_resource(page, per_page):
    response = requests.get(f'https://reqres.in/api/unknown?page={page}&per_page={per_page}')
    assert response.status_code == 200
    assert len(response.json()['data']) > 0

# Негативный тест вывода списка несуществующих ресурсов
def test_get_resource_negative():
    response = requests.get('https://reqres.in/api/unknown999')
    assert response.status_code == 404
    assert response.json()['error'] == 'Not Found'

# позитивный тест для вывода одного ресурса
@pytest.mark.parametrize('resource_id', params_resource_id)
def test_get_resource(resource_id):
    response = requests.get(f'https://reqres.in/api/unknown/{resource_id}')
    assert response.status_code == 200
    assert len(response.json()['data']) > 0

# позитивный тест для вывода одного несуществующего ресурса
@pytest.mark.parametrize('resource_id', params_resource_id_negative)
def test_get_resource_negative(resource_id):
    response = requests.get(f'https://reqres.in/api/unknown/{resource_id}')
    assert response.status_code >= 400


# Позитивный тест: создание пользователя
@pytest.mark.parametrize("name, job", [("Alexey", "IBS"), ("Igor", "Analyst"), ("Maks", "Povar")])
def test_create_user_positive(name, job):
    url = "https://reqres.in/api/users"
    payload = {"name": name, "job": job}
    response = requests.post("https://reqres.in/api/users", data=payload)
    assert response.status_code == 201
    assert response.json()["name"] == name
    assert response.json()["job"] == job


# Позитивный тест: создание пользователя с заполненными дополнительными полями
def test_create_user_payload():
    url = "https://reqres.in/api/users"
    payload = {
        "name": "Alexey",
        "job": "IBS",
        "email": "test@test.com",
        "phone": "123-456-7890"
    }
    response = requests.post(url, data=payload)
    assert response.status_code == 201


# негативные тесты: создание пользователя
@pytest.mark.parametrize("name, job, expected_status_code", [("", "QA", 400), ("Maks", "", 400), ("", "", 400)])
def test_create_user_negative(name, job, expected_status_code):
    payload = {"name": name, "job": job}
    response = requests.post("https://reqres.in/api/users", data=payload)
    assert response.status_code == expected_status_code


# Негативный тест: создание пользователя с пустым payload
def test_create_user_negative():
    url = "https://reqres.in/api/users"
    payload = {
    }
    response = requests.post(url, data=payload)
    assert response.status_code >= 400


# Позитивный тест на обновление данных пользователя PUT
@pytest.mark.parametrize("name, job", [("Alexey", "IBS"), ("Maks", "Povar")])
def test_update_user(name, job):
    response = requests.put(f"https://reqres.in/api/users/2", data={"name": name, "job": job})
    assert response.status_code == 200
    assert response.json()["name"] == name
    assert response.json()["job"] == job


# Негативный тест на обновление данных пользователя PUT
@pytest.mark.parametrize("name, job, status_code", [("", "engineer", 400), ("Jack", "", 400), ("John", "engineer", 200)])
def test_update_user(name, job, status_code):
    url = "https://reqres.in/api/users/2"
    payload = {
        "name": name,
        "job": job
    }
    response = requests.put(url, json=payload)
    assert response.status_code == status_code


# Позитивный тест на обновление данных пользователя PATCH
@pytest.mark.parametrize("name, job", [("Alexey", "IBS"), ("Maks", "Povar")])
def test_update_user(name, job):
    response = requests.patch(f"https://reqres.in/api/users/2", data={"name": name, "job": job})
    assert response.status_code == 200
    assert response.json()["name"] == name
    assert response.json()["job"] == job

# Негативный тест на обновление данных пользователя PATCH
@pytest.mark.parametrize("name, job, status_code", [("", "engineer", 400), ("Jack", "", 400), ("John", "engineer", 200)])
def test_update_user(name, job, status_code):
    url = "https://reqres.in/api/users/2"
    payload = {
        "name": name,
        "job": job
    }
    response = requests.patch(url, json=payload)
    assert response.status_code == status_code


# Позитивный тест на удаление пользователя
@pytest.mark.parametrize("user_id", [(1), (2), (3)])
def test_delete_user_positive(user_id):
    base_url = "https://reqres.in/api/users"
    response = requests.delete(f"{base_url}/{user_id}")
    assert response.status_code == 204


# Негативный тест на удаление пользователя с невалидным id
@pytest.mark.parametrize("user_id", [(0), (-1), ("abc")])
def test_delete_user_negative(user_id):
    base_url = "https://reqres.in/api/users"
    response = requests.delete(f"{base_url}/{user_id}")
    assert response.status_code == 404


# позитивный тест регистрация
@pytest.mark.parametrize("email, password", [("eve.holt@reqres.in", "pistol"), ("tracey.ramos@reqres.in", "123456")])
def test_register_user(email, password):
    response = requests.post("https://reqres.in/api/register", data={"email": email, "password": password})
    assert response.status_code == 200
    assert response.json()["token"] is not None


# позитивный тест невалидные данные при регистрации
@pytest.mark.parametrize("email, password", [("invalid_email", "pistol"), ("", "123456")])
def test_register_user_negative(email, password):
    response = requests.post("https://reqres.in/api/register", data={"email": email, "password": password})
    assert response.status_code == 400


# Позитивный тест - успешный логин
@pytest.mark.parametrize('email, password', [('eve.holt@reqres.in', 'cityslicka')])
def test_login(email, password):
    url = 'https://reqres.in/api/login'
    payload = {'email': email, 'password': password}
    response = requests.post(url, data=payload)
    assert response.status_code == 200
    assert 'token' in response.json()


# Негативный тест - логин с неправильным email
@pytest.mark.parametrize('email, password', [('test', 'password')])
def test_login_negative_email(email, password):
    url = 'https://reqres.in/api/login'
    payload = {'email': email, 'password': password}
    response = requests.post(url, data=payload)
    assert response.status_code == 400


# Негативный тест - логин с неправильным password
@pytest.mark.parametrize('email, password', [('kols.dsds@test.in', 'test')])
def test_login_negative_password(email, password):
    url = 'https://reqres.in/api/login'
    payload = {'email': email, 'password': password}
    response = requests.post(url, data=payload)
    assert response.status_code == 400
    assert response.json()['error'] == 'Missing password'


# Фикстура
@pytest.fixture(params=[0, 1, 2])
def delay_param(request):
    return request.param

# Позитивный - дилей
def test_get_users_with_delay_positive(delay_param):
    url = f"https://reqres.in/api/users?delay={delay_param}"
    response = requests.get(url)
    assert response.status_code == 200
    assert "data" in response.json()

# негативный - дилей
def test_get_users_with_delay_negative(delay_param):
    url = f"https://reqres.in/api/users?delay={delay_param}"
    response = requests.get(url)
    assert response.status_code == 404
    assert response.json() == {}