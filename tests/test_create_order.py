import allure

from messages import Messages


@allure.suite("Создание заказа")
class TestCreateOrder:
    @allure.title("Создание заказа для авторизованного пользователя с валидными ингредиентами")
    def test_create_order_authorized_user_with_ingredients_success(self, order_client, ingredients_setup, user_client,
                                                                   user_setup):
        user_client.set_access_token(user_setup["access_token"])

        response = order_client.create_order(ingredients_setup)
        res_json = response.json()

        with allure.step("Проверка кода ответа"):
            assert response.status_code == 200

        with allure.step("Проверка тела ответа"):
            assert res_json.get("success") is True
            assert "number" in res_json.get("order", {})

    @allure.title("Создание заказа для неавторизованного пользователя с валидными ингредиентами")
    def test_create_order_unauthorized_user_with_ingredients_success(self, order_client, ingredients_setup):
        response = order_client.create_order(ingredients_setup)
        res_json = response.json()

        with allure.step("Проверка кода ответа"):
            assert response.status_code == 200

        with allure.step("Проверка тела ответа"):
            assert res_json.get("success") is True
            assert "number" in res_json.get("order", {})

    @allure.title("Создание заказа для авторизированного пользователя без ингредиентов")
    def test_create_order_authorized_user_without_ingredients_shows_error(self, order_client, user_client, user_setup):
        user_client.set_access_token(user_setup["access_token"])

        with allure.step("Формирование пустого листа ингредиентов для заказа"):
            payload = {"ingredients": []}

        response = order_client.create_order(payload)
        res_json = response.json()

        with allure.step("Проверка кода ответа"):
            assert response.status_code == 400

        with allure.step("Проверка тела ответа"):
            assert res_json.get("success") is False
            assert res_json.get("message") == Messages.EMPTY_INGREDIENTS_FOR_CREATE_ORDER

    @allure.title("Создание заказа для авторизированного пользователя с невалидными ингредиентами")
    def test_create_order_authorized_user_incorrect_ingredients_shows_error(self, order_client, user_client, user_setup,
                                                                            ingredients_with_invalid_hash):
        user_client.set_access_token(user_setup["access_token"])

        response = order_client.create_order(ingredients_with_invalid_hash)

        with allure.step("Проверка кода ответа"):
            assert response.status_code == 500

        with allure.step("Проверка тела ответа"):
            assert Messages.INTERNAL_SERVER_ERROR in response.text
