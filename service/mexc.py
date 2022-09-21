from requests import get


class MexcService:

    def __init__(self):
        self.url = "https://www.mexc.com/open/api/v2/market/depth"


    def start(self,from_,to):
        PARAMS = {"symbol": f"{from_}_{to}", "depth": "1"}
        resp = get(self.url, params=PARAMS)
        inch_data = resp.json()
        return inch_data