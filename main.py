import requests
from datetime import datetime, timedelta
import time
import json
import re
import setting
import github

GITHUB_TOKEN = setting.GITHUB_ACCESS_TOKEN
g = github.Github(GITHUB_TOKEN)


def get_exchange():
    response = requests.get(
        "https://api.cryptowat.ch/exchanges")
    data = response.json()
    return data["result"]


def get_markets(url):
    response = requests.get(url)
    data = response.json()
    return data["result"]


def get_price(url, min, before=0, after=0):
    price = []
    params = {"periods": min}
    if before != 0:
        params["before"] = before
    if after != 0:
        params["after"] = after

    response = requests.get(
        url, params)
    data = response.json()

    if "result" not in data:
        return

    if data["result"][str(min)] is not None:
        for i in data["result"][str(min)]:
            price.append(
                {
                    "close_time": i[0],
                    "close_time_dt": datetime.fromtimestamp(
                        i[0]).strftime('%Y/%m/%d %H:%M'),
                    "open_price": i[1],
                    "high_price": i[2],
                    "low_price": i[3],
                    "close_price": i[4]})

        matches = re.match(
            r'.+://.+/(.+)/(.+)/.+', url).groups()
        print(matches)
        markets_name = matches[0]
        exchange_name = matches[1]
        if price is not None:
            try:
                repo = g.get_repo("Ny-uta/crypto_price_data")
                repo.create_file(
                    f"{markets_name}/{exchange_name}/{price[0]['close_time']}.json",
                    "content_of_file",
                    json.dumps(
                        price,
                        indent=2))
            except Exception as e:
                print(e)
                print(response)
        return

    else:
        print("データが存在しません")
        return None


# ここからメイン
file = open("target.json", "r")
json_load = json.load(file)

# データ取得日時を現在時刻-1Hで行う
start_time = datetime.now().replace(second=0, microsecond=0) + \
    timedelta(hours=-24, minutes=-10)

end_time = datetime.now().replace(second=0, microsecond=0) + \
    timedelta(hours=0, minutes=+10)

print(str(start_time.timestamp()).replace('.0', ''))
print(str(end_time.timestamp()).replace('.0', ''))


for exchange in json_load:
    currency_list = exchange["currency"]
    for currency in currency_list:
        get_price(
            currency["route"] +
            "/ohlc",
            60,
            after=str(
                start_time.timestamp()).replace(
                '.0',
                ''),
            before=str(
                end_time.timestamp()).replace(
                    '.0',
                ''))
        time.sleep(2)
