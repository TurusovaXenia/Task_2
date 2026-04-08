from clients.base_client import BaseClient
from endpoints import Endpoints


class OrderClient(BaseClient):
    def create_order(self, payload, token=None):
        return self.post(Endpoints.CREATE_ORDER, payload, headers=self._get_headers(token))

    def get_ingredients(self):
        return self.get(Endpoints.GET_INGREDIENTS)
