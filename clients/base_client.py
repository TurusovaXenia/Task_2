class BaseClient:
    def __init__(self, base_url, session):
        self.base_url = base_url
        self.session = session

    def set_token(self, token):
        self.session.headers.update({"Authorization": {token}})

    def post(self, url, payload):
        return self.session.post(self.base_url + url, data=payload)

    def delete(self, url, headers):
        return self.session.delete(self.base_url + url, headers=headers)
