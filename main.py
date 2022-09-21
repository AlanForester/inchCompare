import json
from os import getcwd
from service import InchService
if __name__ == '__main__':
    with open(f'{getcwd()}/service/files/inch.json') as json_data:
        d = json.load(json_data)
        data = d.get("tokens")
        print(bool(data))
        InchService(data)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
