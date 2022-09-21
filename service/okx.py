from requests import get


class OkxService:
    def __init__(self):
        self.url = "https://www.okx.com/api/v5/market/books"

    def start(self, from_, to):
        PARAMS = {"instId": f"{from_}-{to}"}
        resp = get(self.url, params=PARAMS)
        inch_data = resp.json()
        return inch_data
