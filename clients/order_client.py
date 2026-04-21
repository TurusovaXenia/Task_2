import allure

from clients.base_client import BaseClient
from endpoints import Endpoints


class OrderClient(BaseClient):
    @allure.step("Отправка POST-запроса для создания заказа")
    def create_order(self, payload, token=None):
        return self.post(Endpoints.CREATE_ORDER, payload, headers=self._get_headers(token))

    @allure.step("Отправка GET-запроса для получения доступных ингредиентов")
    def get_ingredients(self):
        return self.get(Endpoints.GET_INGREDIENTS)

    @allure.step("Отправка GET-запроса для получения заказов пользователя")
    def get_orders_for_user(self, token=None):
        return self.get(Endpoints.GET_ORDERS_FOR_USER, headers=self._get_headers(token))
