import pytest
import requests

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
    token_box = []
    yield token_box
    if token_box:
        user_client.delete_user(token_box[0])
