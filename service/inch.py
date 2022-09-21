from requests import get
from .mexc import MexcService
from .kucoin import KucoinService
from .gate import GateService
from .bitrue import BitrueService
from .okx import OkxService
import json
from datetime import datetime


class InchService:
    def __init__(self, data):
        self.data = data
        self.url = "https://api.1inch.io/v4.0/1/quote"
        self.back_data = {}
        self.mexc = MexcService()
        self.kucoin = KucoinService()
        self.gate = GateService()
        self.bitrue = BitrueService()
        self.okx = OkxService()
        self.start()

    def start(self):
        x = 0
        xx = len(self.data)
        for to_key, to_value in self.data.items():
            print(f"{x} из {xx}")
            x += 1
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
                self.back_data[f"{from_}_{to}"] = {"inch": int(inch_return) / 1000000000000000000}

            mexc_data_from = self.mexc.start(f"{to}", f"{from_}")
            if mexc_return := mexc_data_from.get("data"):
                if self.back_data.get(f"{to}_{from_}"):
                    self.back_data[f"{to}_{from_}"].update({"mexc": mexc_return.get("asks")[0]["price"]})
                else:
                    self.back_data[f"{to}_{from_}"] = {"mexc": mexc_return.get("asks")[0]["price"]}
                print(mexc_return)

            mexc_data_to = self.mexc.start(f"{from_}", f"{to}")
            if mexc_return := mexc_data_to.get("data"):
                if self.back_data.get(f"{from_}_{to}"):
                    self.back_data[f"{from_}_{to}"].update({"mexc": mexc_return.get("asks")[0]["price"]})
                else:
                    self.back_data[f"{from_}_{to}"] = {"mexc": mexc_return.get("asks")[0]["price"]}
                print(mexc_return)

            kucoin_data_to = self.kucoin.start(from_, to)
            if kucoin_return_to := kucoin_data_to.get("data"):
                if self.back_data.get(f"{from_}_{to}"):
                    self.back_data[f"{from_}_{to}"].update({"kucoin": kucoin_return_to.get("price")})
                else:
                    self.back_data[f"{from_}_{to}"] = {"kucoin": kucoin_return_to.get("price")}
                print(kucoin_data_to)
            kucoin_data_from = self.kucoin.start(to, from_)
            if kucoin_return_from := kucoin_data_from.get("data"):
                if self.back_data.get(f"{to}_{from_}"):
                    self.back_data[f"{to}_{from_}"].update({"kucoin": kucoin_return_from.get("price")})
                else:
                    self.back_data[f"{to}_{from_}"] = {"kucoin": kucoin_return_from.get("price")}
                print(kucoin_data_from)

            gate_data_to = self.gate.start(from_, to)
            if gate_return_to := gate_data_to.get("asks"):
                if self.back_data.get(f"{from_}_{to}"):
                    self.back_data[f"{from_}_{to}"].update({"gate": gate_return_to[0][0]})
                else:
                    self.back_data[f"{from_}_{to}"] = {"gate": gate_return_to[0][0]}
                print(gate_data_to)
            gate_data_from = self.gate.start(to, from_)
            if gate_return_from := gate_data_from.get("asks"):
                if self.back_data.get(f"{to}_{from_}"):
                    self.back_data[f"{to}_{from_}"].update({"gate": gate_return_from[0][0]})
                else:
                    self.back_data[f"{to}_{from_}"] = {"gate": gate_return_from[0][0]}
                print(gate_data_from)

            bitrue_data_to = self.bitrue.start(from_, to)
            if bitrue_return_to := bitrue_data_to.get("askPrice"):
                if self.back_data.get(f"{from_}_{to}"):
                    self.back_data[f"{from_}_{to}"].update({"bitrue": bitrue_return_to})
                else:
                    self.back_data[f"{from_}_{to}"] = {"bitrue": bitrue_return_to}
                print(bitrue_data_to)
            bitrue_data_from = self.bitrue.start(to, from_)
            if bitrue_return_from := bitrue_data_from.get("askPrice"):
                if self.back_data.get(f"{to}_{from_}"):
                    self.back_data[f"{to}_{from_}"].update({"bitrue": bitrue_return_from})
                else:
                    self.back_data[f"{to}_{from_}"] = {"bitrue": bitrue_return_from}
                print(bitrue_data_from)

            okx_data_to = self.okx.start(from_, to)
            if okx_return_to := okx_data_to.get("data"):
                if self.back_data.get(f"{from_}_{to}"):
                    self.back_data[f"{from_}_{to}"].update({"okx": okx_return_to[0].get("asks")[0][0]})
                else:
                    self.back_data[f"{from_}_{to}"] = {"okx": okx_return_to[0].get("asks")[0][0]}
                print(okx_data_to)
            okx_data_from = self.okx.start(to, from_)
            if okx_return_from := okx_data_from.get("data"):
                if self.back_data.get(f"{to}_{from_}"):
                    self.back_data[f"{to}_{from_}"].update({"okx": okx_return_from[0].get("asks")[0][0]})
                else:
                    self.back_data[f"{to}_{from_}"] = {"okx": okx_return_from[0].get("asks")[0][0]}
                print(okx_data_from)
        with open(f"{datetime.now()}.json", "w") as fp:
            json.dump(self.back_data, fp)
