from clients.base_client import BaseClient
from endpoints import Endpoints


class UserClient(BaseClient):
    def create_user(self, payload):
        return self.post(Endpoints.CREATE_USER, payload)

    def delete_user(self, token):
        return self.delete(Endpoints.DELETE_USER, headers={"Authorization": token})
