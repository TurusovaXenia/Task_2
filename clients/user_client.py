import allure

from clients.base_client import BaseClient
from endpoints import Endpoints


class UserClient(BaseClient):
    @allure.step("Отправка POST-запроса для создания пользователя")
    def create_user(self, payload):
        return self.post(Endpoints.CREATE_USER, payload)

    @allure.step("Отправка DELETE-запроса для удаления пользователя")
    def delete_user(self, token=None):
        headers = self._get_headers(token)
        return self.delete(Endpoints.DELETE_USER, headers=headers)

    @allure.step("Отправка POST-запроса для авторизации пользователя")
    def login_user(self, email, password):
        payload = {
            "email": email,
            "password": password
        }
        return self.post(Endpoints.LOGIN_USER, payload)

    @allure.step("Отправка PATCH-запроса для обновления данных пользователя")
    def update_user(self, payload, token=None):
        return self.patch(Endpoints.UPDATE_USER, payload, headers=self._get_headers(token))
