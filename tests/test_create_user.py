import pytest

import data
from messages import Messages


class TestCreateUser:
    def test_create_unique_user_success(self, user_client, new_user_data, user_cleanup):
        response = user_client.create_user(new_user_data)
        res_json = response.json()
        user_cleanup.append(res_json.get("accessToken"))

        assert response.status_code == 200
        assert res_json.get("success") is True

    def test_create_user_duplicate_shows_error(self, user_client, new_user_data, user_cleanup):
        response = user_client.create_user(new_user_data)
        user_cleanup.append(response.json().get("accessToken"))
        response = user_client.create_user(new_user_data)
        res_json = response.json()

        assert response.status_code == 403
        assert res_json.get("success") is False
        assert res_json.get("message") == Messages.USER_ALREADY_REGISTERED

    @pytest.mark.parametrize("empty_field", ["email", "password", "name"])
    def test_create_user_empty_fields_shows_error(self, user_client, empty_field):
        user_data = data.valid_user_data.copy()
        user_data[empty_field] = ''
        response = user_client.create_user(user_data)
        res_json = response.json()

        assert response.status_code == 403
        assert res_json.get("success") is False
        assert res_json.get("message") == Messages.MISSING_FIELD_ON_REGISTRATION
