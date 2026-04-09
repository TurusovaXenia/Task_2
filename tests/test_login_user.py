import allure
import pytest

from messages import Messages


@allure.suite("Авторизация пользователя")
class TestLoginUser:
    @allure.title("Успешная авторизация пользователя")
    def test_login_user_success(self, user_client, user_setup):
        response = user_client.login_user(user_setup["email"], user_setup["password"])
        res_json = response.json()

        with allure.step("Проверка кода ответа"):
            assert response.status_code == 200

        with allure.step("Проверка тела ответа"):
            assert res_json.get("success") is True
            assert res_json.get("user", {}).get("email") == user_setup["email"]
            assert res_json.get("user", {}).get("name") == user_setup["name"]

    @pytest.mark.parametrize("incorrect_field", ["email", "password"])
    @allure.title("Авторизация пользователя с неверным логином/паролем")
    def test_login_user_incorrect_fields_show_error(self, user_client, user_setup, incorrect_field):
        with allure.step(f"Подмена поля {incorrect_field} на невалидное значение"):
            user_data = user_setup.copy()
            user_data[incorrect_field] = f"incorrect {incorrect_field}"

        response = user_client.login_user(user_data["email"], user_data["password"])
        res_json = response.json()

        with allure.step("Проверка кода ответа"):
            assert response.status_code == 401

        with allure.step("Проверка тела ответа"):
            assert res_json.get("success") is False
            assert res_json.get("message") == Messages.MISSING_FIELD_ON_LOGIN
