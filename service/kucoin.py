from requests import get


class KucoinService:

    def __init__(self):
        self.url = "https://api.kucoin.com/api/v1/market/orderbook/level1"


    def start(self,from_,to):
        PARAMS = {"symbol": f"{from_}-{to}"}
        resp = get(self.url, params=PARAMS)
        inch_data = resp.json()
        return inch_data