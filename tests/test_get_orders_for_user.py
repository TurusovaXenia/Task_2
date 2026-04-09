import allure

from messages import Messages


@allure.suite("Получение заказов для пользователя")
class TestGetOrdersForUser:
    @allure.title("Получение заказов для авторизованного пользователя")
    def test_get_orders_for_user_authorized_user_success(self, user_token_with_created_order, order_client):
        response = order_client.get_orders_for_user(user_token_with_created_order)
        res_json = response.json()

        with allure.step("Проверка кода ответа"):
            assert response.status_code == 200

        with allure.step("Проверка тела ответа"):
            assert res_json.get("success") is True
            assert "orders" in res_json

    @allure.title("Получение заказов для неавторизованного пользователя")
    def test_get_orders_for_user_unauthorized_user_shows_error(self, order_client):
        response = order_client.get_orders_for_user()
        res_json = response.json()

        with allure.step("Проверка кода ответа"):
            assert response.status_code == 401

        with allure.step("Проверка тела ответа"):
            assert res_json.get("success") is False
            assert res_json.get("message") == Messages.UNAUTHORIZED_ON_GET_ORDERS_FOR_USER
