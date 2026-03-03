import requests

class Client:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    def get(self, endpoint, **kwargs):
        return self.session.get(f"{self.base_url}{endpoint}", **kwargs)

    def post(self, endpoint, **kwargs):
        return self.session.post(f"{self.base_url}{endpoint}", **kwargs)

    def put(self, endpoint, json=None):
        return self.session.put(f"{self.base_url}{endpoint}", json=json)

    def delete(self, endpoint):
        return self.session.delete(f"{self.base_url}{endpoint}")
