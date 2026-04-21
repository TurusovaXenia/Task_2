import allure
import pytest
import requests

from clients.order_client import OrderClient
from clients.user_client import UserClient
from endpoints import Endpoints
from utils import helpers


@pytest.fixture(scope="session")
def api_session():
    session = requests.Session()
    yield session
    session.close()


@pytest.fixture(scope="function")
def user_client(api_session):
    return UserClient(Endpoints.BASE_URL, api_session)


@pytest.fixture(scope="function")
def new_user_data():
    new_user_data = helpers.generate_new_user()
    return new_user_data


@pytest.fixture(scope="function")
def user_cleanup(user_client):
    access_token_box = []
    yield access_token_box
    if access_token_box:
        user_client.delete_user(access_token_box[0])


@pytest.fixture(scope="function")
def user_setup(user_client, new_user_data):
    with allure.step("Подготовка пользователя"):
        response = user_client.create_user(new_user_data)
        access_token = response.json().get("accessToken")

        setup_data = {
            "access_token": access_token,
            "name": new_user_data["name"],
            "email": new_user_data["email"],
            "password": new_user_data["password"],
        }

        yield setup_data

        with allure.step("Удаление пользователя"):
            if access_token:
                user_client.delete_user(access_token)


@pytest.fixture(scope="function")
def order_client(api_session):
    return OrderClient(Endpoints.BASE_URL, api_session)


@pytest.fixture(scope="function")
def ingredients_setup(order_client):
    with allure.step("Подготовка ингредиентов для создания заказа"):
        response = order_client.get_ingredients()
        items = response.json()["data"][:3]
        payload = {
            "ingredients": [item["_id"] for item in items]
        }
        return payload


@pytest.fixture(scope="function")
def ingredients_with_invalid_hash():
    with allure.step("Генерация невалидных ингредиентов для заказа"):
        payload = {"ingredients": [helpers.generate_random_string(5)]}
        return payload


@pytest.fixture(scope="function")
def user_token_with_created_order(user_setup, ingredients_setup, user_client, order_client):
    with allure.step("Подготовка пользователя с заказом"):
        with allure.step("Авторизация пользователя"):
            user_client.set_access_token(user_setup["access_token"])

        with allure.step("Создание заказа для пользователя"):
            order_client.create_order(ingredients_setup)

        return user_setup["access_token"]
