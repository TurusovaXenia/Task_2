import pytest

from messages import Messages


class TestLoginUser:
    def test_login_user_success(self, user_client, user_setup):
        response = user_client.login_user(user_setup["email"], user_setup["password"])

        assert response.status_code == 200
        assert response.json().get("success") is True

    @pytest.mark.parametrize("incorrect_field", ["email", "password"])
    def test_login_user_incorrect_fields_show_error(self, user_client, user_setup, incorrect_field):
        user_data = user_setup.copy()
        user_data[incorrect_field] = f"incorrect {incorrect_field}"
        response = user_client.login_user(user_data["email"], user_data["password"])
        res_json = response.json()

        assert response.status_code == 401
        assert res_json.get("success") is False
        assert res_json.get("message") == Messages.MISSING_FIELD_ON_LOGIN
