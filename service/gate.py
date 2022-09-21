from requests import get


class GateService:
    def __init__(self):
        self.url = "https://api.gateio.ws/api/v4/spot/order_book"

    def start(self, from_, to):
        PARAMS = {"currency_pair": f"{from_}_{to}", "depth": "1"}
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        resp = get(self.url, params=PARAMS, headers=headers)
        inch_data = resp.json()
        return inch_data
