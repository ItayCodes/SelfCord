import requests


class HTTPClient:
    def __init__(self, token: str):
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": token,
            "Content-Type": "application/json"
        })

    def request(self, method: str, endpoint: str, json: dict = None, params: dict = None):
        url = f"https://discord.com/api/v10/{endpoint}"
        response = self.session.request(method, url, json=json, params=params)
        return response
