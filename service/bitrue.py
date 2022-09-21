from requests import get


class BitrueService:
    def __init__(self):
        self.url = "https://openapi.bitrue.com/api/v1/ticker/bookTicker"

    def start(self, from_, to):
        PARAMS = {"symbol": f"{from_}{to}"}
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        resp = get(self.url, params=PARAMS, headers=headers)
        inch_data = resp.json()
        return inch_data
