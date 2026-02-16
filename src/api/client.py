import requests

class Client:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    def get(self, endpoint):
        return self.session.get(f"{self.base_url}{endpoint}")

    def post(self, endpoint):
        return self.session.post(f"{self.base_url}{endpoint}")

    def put(self, endpoint):
        return self.session.put(f"{self.base_url}{endpoint}")

    def delete(self, endpoint):
        return self.session.delete(f"{self.base_url}{endpoint}")
