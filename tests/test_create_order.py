from messages import Messages


class TestCreateOrder:
    def test_create_order_authorized_user_with_ingredients_success(self, order_client, ingredients_setup, user_client,
                                                                   user_setup):
        user_client.set_token(user_setup["access_token"])

        response = order_client.create_order(ingredients_setup)
        res_json = response.json()

        assert response.status_code == 200
        assert res_json.get("success") is True
        assert "order" in res_json

    def test_create_order_unauthorized_user_with_ingredients_success(self, order_client, ingredients_setup):
        response = order_client.create_order(ingredients_setup)
        res_json = response.json()

        assert response.status_code == 200
        assert res_json.get("success") is True
        assert "order" in res_json

    def test_create_order_authorized_user_without_ingredients_shows_error(self, order_client, user_client, user_setup):
        user_client.set_token(user_setup["access_token"])
        payload = {"ingredients": []}

        response = order_client.create_order(payload)
        res_json = response.json()

        assert response.status_code == 400
        assert res_json.get("success") is False
        assert res_json.get("message") == Messages.EMPTY_INGREDIENTS_FOR_CREATE_ORDER

    def test_create_order_authorized_user_incorrect_ingredients_shows_error(self, order_client, user_client, user_setup,
                                                                            order_with_invalid_hash):
        user_client.set_token(user_setup["access_token"])
        response = order_client.create_order(order_with_invalid_hash)
        assert response.status_code == 500
