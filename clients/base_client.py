class BaseClient:
    def __init__(self, base_url, session):
        self.base_url = base_url
        self.session = session
        self.token = None

    def set_token(self, token):
        self.token = token

    def _get_headers(self, manual_token=None):
        target = manual_token if manual_token is not None else self.token

        headers = {}
        if target:
            headers["Authorization"] = target
        return headers

    def post(self, url, payload, headers=None):
        return self.session.post(self.base_url + url, data=payload, headers=headers)

    def delete(self, url, headers):
        return self.session.delete(self.base_url + url, headers=headers)

    def patch(self, url, payload, headers):
        return self.session.patch(self.base_url + url, data=payload, headers=headers)

    def get(self, url):
        return self.session.get(self.base_url + url)
