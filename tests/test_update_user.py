import allure
import pytest

from messages import Messages


@allure.suite("Изменение данных пользователя")
class TestUpdateUser:
    @pytest.mark.parametrize("field_to_modify", ["email", "password", "name"])
    @allure.title("Успешное изменение данных авторизованного пользователя")
    def test_update_user_authorized_user_success(self, user_client, user_setup, field_to_modify):
        with allure.step(f"Изменение поля {field_to_modify}"):
            user_data = user_setup.copy()
            user_data[field_to_modify] = f"new_{user_data[field_to_modify]}"

        user_client.set_access_token(user_data["access_token"])

        response = user_client.update_user(user_data)
        res_json = response.json()

        with allure.step("Проверка кода ответа"):
            assert response.status_code == 200

        with allure.step("Проверка тела ответа"):
            assert res_json.get("success") is True
            assert res_json.get('user', {}).get('email') == user_data["email"]
            assert res_json.get('user', {}).get('name') == user_data["name"]

    @pytest.mark.parametrize("field_to_modify", ["email", "password", "name"])
    @allure.title("Проверка невозможности изменить данные для неавторизованного пользователя")
    def test_update_user_unauthorized_user_shows_error(self, user_client, user_setup, field_to_modify):
        with allure.step(f"Изменение поля {field_to_modify}"):
            user_data = user_setup.copy()
            user_data[field_to_modify] = f"new_{user_data[field_to_modify]}"

        response = user_client.update_user(user_data)
        res_json = response.json()

        with allure.step("Проверка кода ответа"):
            assert response.status_code == 401

        with allure.step("Проверка тела ответа"):
            assert res_json.get("success") is False
            assert res_json.get("message") == Messages.UNAUTHORIZED_ON_USER_UPDATE
