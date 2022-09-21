from requests import get
from .mexc import MexcService
from .kucoin import KucoinService

class InchService:
    def __init__(self, data):
        self.data = data
        self.url = "https://api.1inch.io/v4.0/1/quote"
        self.back_data = {}
        self.mexc = MexcService()
        self.kucoin = KucoinService()
        self.start()

    def start(self):
        for to_key, to_value in self.data.items():
            PARAMS = {
                "fromTokenAddress": "0xdac17f958d2ee523a2206206994597c13d831ec7",
                "toTokenAddress": to_key,
                "amount": "10000000000000000",
            }
            from_ = "USDT"
            to = f"{to_value.get('symbol')}"
            resp = get(self.url, params=PARAMS)

            inch_data = resp.json()
            print(inch_data)
            if inch_return := inch_data.get("toTokenAmount"):
                self.back_data[f"{from_}_{to}"] = {
                    "inch": int(inch_return) / 1000000000000000000
                }
            mexc_data = self.mexc.start(f"{to_value.get('symbol')}", "USDT")
            if mexc_return := mexc_data.get("data"):
                if self.back_data.get(f"{from_}_{to}"):
                    self.back_data[f"{from_}_{to}"].update(
                        {"mexc": mexc_return.get("bids")[0]["price"]}
                    )
                else:
                    self.back_data[f"{from_}_{to}"] = {
                        "mexc": mexc_return.get("bids")[0]["price"]
                    }
                if self.back_data.get(f"{to}_{from_}"):
                    self.back_data[f"{to}_{from_}"].update(
                        {"mexc": mexc_return.get("asks")[0]["price"]}
                    )
                else:
                    self.back_data[f"{to}_{from_}"] = {
                        "mexc": mexc_return.get("asks")[0]["price"]
                    }
                print(mexc_return)
            kucoin_data_to = self.kucoin.start(from_,to)
            if kucoin_return_to := kucoin_data_to.get("data"):
                if self.back_data.get(f"{from_}_{to}"):
                    self.back_data[f"{from_}_{to}"].update(
                        {"kucoin": kucoin_return_to.get("price")}
                    )
                else:
                    self.back_data[f"{from_}_{to}"] = {"kucoin": kucoin_return_to.get("price")}
                print(kucoin_data_to)
            kucoin_data_from = self.kucoin.start(to,from_)
            if kucoin_return_from := kucoin_data_from.get("data"):
                if self.back_data.get(f"{from_}_{to}"):
                    self.back_data[f"{from_}_{to}"].update(
                        {"kucoin": kucoin_return_from.get("price")}
                    )
                else:
                    self.back_data[f"{from_}_{to}"] = {"kucoin": kucoin_return_from.get("price")}
                print(kucoin_data_from)



