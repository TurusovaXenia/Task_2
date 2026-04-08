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
    response = user_client.create_user(new_user_data)
    access_token = response.json().get("accessToken")

    setup_data = {
        "access_token": access_token,
        "name": new_user_data["name"],
        "email": new_user_data["email"],
        "password": new_user_data["password"],
    }
    yield setup_data

    if access_token:
        user_client.delete_user(access_token)


@pytest.fixture(scope="function")
def order_client(api_session):
    return OrderClient(Endpoints.BASE_URL, api_session)


@pytest.fixture(scope="function")
def ingredients_setup(order_client):
    response = order_client.get_ingredients()
    items = response.json()["data"][:3]
    payload = {
        "ingredients": [item["_id"] for item in items]
    }
    return payload


@pytest.fixture(scope="function")
def order_with_invalid_hash():
    payload = {"ingredients": [helpers.generate_random_string(5)]}
    return payload
