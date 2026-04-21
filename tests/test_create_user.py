import allure
import pytest

import data
from messages import Messages


@allure.suite("Создание пользователя")
class TestCreateUser:
    @allure.title("Успешное создание уникального пользователя")
    def test_create_unique_user_success(self, user_client, new_user_data, user_cleanup):
        response = user_client.create_user(new_user_data)
        res_json = response.json()
        user_cleanup.append(res_json.get("accessToken"))

        with allure.step("Проверка кода ответа"):
            assert response.status_code == 200

        with allure.step("Проверка тела ответа"):
            assert res_json.get("success") is True
            assert res_json.get("user", {}).get("email") == new_user_data["email"]
            assert res_json.get("user", {}).get("name") == new_user_data["name"]

    @allure.title("Создание пользователя, который уже зарегистрирован")
    def test_create_user_duplicate_shows_error(self, user_client, new_user_data, user_cleanup):
        with allure.step("Создаем первого пользователя"):
            response_1 = user_client.create_user(new_user_data)
            user_cleanup.append(response_1.json().get("accessToken"))

        with allure.step("Создаем второго пользователя с данными первого пользователя"):
            response_2 = user_client.create_user(new_user_data)
            res_json = response_2.json()

        with allure.step("Проверка кода ответа"):
            assert response_2.status_code == 403

        with allure.step("Проверка тела ответа"):
            assert res_json.get("success") is False
            assert res_json.get("message") == Messages.USER_ALREADY_REGISTERED

    @pytest.mark.parametrize("empty_field", ["email", "password", "name"])
    @allure.title("Проверка невозможности создания пользователя если обязательные поля отсутствуют в запросе")
    def test_create_user_empty_fields_shows_error(self, user_client, empty_field):
        with allure.step(f"Очистка поля {empty_field}"):
            user_data = data.valid_user_data.copy()
            user_data[empty_field] = ""

        response = user_client.create_user(user_data)
        res_json = response.json()

        with allure.step("Проверка кода ответа"):
            assert response.status_code == 403

        with allure.step("Проверка тела ответа"):
            assert res_json.get("success") is False
            assert res_json.get("message") == Messages.MISSING_FIELD_ON_REGISTRATION
