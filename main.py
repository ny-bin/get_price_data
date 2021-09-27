import requests
from datetime import datetime, timedelta
import time
import json
import re
import setting
import github

GITHUB_TOKEN = setting.GITHUB_ACCESS_TOKEN
BYBT_TOKEN = setting.BYBT_ACCESS_TOKEN
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


def get_OI(start_time, symbol):
    url = 'https://open-api.bybt.com'
    endpoint = f'/api/pro/v1/futures/openInterest/chart?interval=2&symbol={symbol}'
    params = {}
    headers = {
        'bybtSecret': BYBT_TOKEN
    }
    response = requests.request(
        "GET",
        url + endpoint,
        headers=headers,
        data=params)
    json_res = json.loads(response.text)
    if json_res['msg'] == 'success':
        # githubに書き込み
        try:
            repo = g.get_repo("Ny-uta/crypto_price_data")
            repo.create_file(
                f"openInterst/{symbol}/{start_time}.json",
                "content_of_file",
                json.dumps(
                    json_res['data'],
                    indent=2))
        except Exception as e:
            print(e)
            print(response)
    return


def get_liquidataion(start_time, symbol):
    url = 'https://open-api.bybt.com'
    endpoint = f'/api/pro/v1/futures/liquidation/detail/chart?timeType=11&symbol={symbol}'
    params = {}
    headers = {
        'bybtSecret': BYBT_TOKEN
    }
    response = requests.request(
        "GET",
        url + endpoint,
        headers=headers,
        data=params)
    json_res = json.loads(response.text)
    if json_res['msg'] == 'success':
        # githubに書き込み
        try:
            repo = g.get_repo("Ny-uta/crypto_price_data")
            repo.create_file(
                f"Liquidation/{symbol}/{start_time}.json",
                "content_of_file",
                json.dumps(
                    json_res['data'],
                    indent=2))
        except Exception as e:
            print(e)
            print(response)
    return


def get_longshort(start_time, symbol):
    url = 'https://open-api.bybt.com'
    endpoint = f'/api/pro/v1/futures/longShort_chart?interval=2&symbol={symbol}'
    params = {}
    headers = {
        'bybtSecret': BYBT_TOKEN
    }
    response = requests.request(
        "GET",
        url + endpoint,
        headers=headers,
        data=params)
    json_res = json.loads(response.text)
    if json_res['msg'] == 'success':
        # githubに書き込み
        try:
            repo = g.get_repo("Ny-uta/crypto_price_data")
            repo.create_file(
                f"LognShort/{symbol}/{start_time}.json",
                "content_of_file",
                json.dumps(
                    json_res['data'],
                    indent=2))
        except Exception as e:
            print(e)
            print(response)
    return


def get_FR(start_time, symbol):
    url = 'https://open-api.bybt.com'
    endpoint = f'/api/pro/v1/futures/funding_rates_chart?symbol={symbol}'
    params = {}
    headers = {
        'bybtSecret': BYBT_TOKEN
    }
    response = requests.request(
        "GET",
        url + endpoint,
        headers=headers,
        data=params)
    json_res = json.loads(response.text)
    if json_res['msg'] == 'success':
        # githubに書き込み
        try:
            repo = g.get_repo("Ny-uta/crypto_price_data")
            repo.create_file(
                f"FR/{symbol}/{start_time}.json",
                "content_of_file",
                json.dumps(
                    json_res['data'],
                    indent=2))
        except Exception as e:
            print(e)
            print(response)
    return


def get_Vol(start_time, symbol):
    url = 'https://open-api.bybt.com'
    endpoint = f'/api/pro/v1/futures/vol/chart?symbol={symbol}'
    params = {}
    headers = {
        'bybtSecret': BYBT_TOKEN
    }
    response = requests.request(
        "GET",
        url + endpoint,
        headers=headers,
        data=params)
    json_res = json.loads(response.text)
    if json_res['msg'] == 'success':
        # githubに書き込み
        try:
            repo = g.get_repo("Ny-uta/crypto_price_data")
            repo.create_file(
                f"Vol/{symbol}/{start_time}.json",
                "content_of_file",
                json.dumps(
                    json_res['data'],
                    indent=2))
        except Exception as e:
            print(e)
            print(response)
    return

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


currency_list = ["BTC", "ETH", "EOS", "BCH", "LTC", "XRP"]

for currency in currency_list:
    # OI
    get_OI(start_time.strftime('%Y_%m_%d_1H'), currency)
    time.sleep(1)
    # 清算
    get_liquidataion(start_time.strftime('%Y_%m_%d_30m'), currency)
    time.sleep(1)

    # FR
    get_FR(start_time.strftime('%Y_%m_%d_C'), currency)

    # Vol
    get_Vol(start_time.strftime('%Y_%m_%d_V'), currency)

    if currency in ["BTC", "ETH", "EOS"]:
        # L/S比率
        get_longshort(start_time.strftime('%Y_%m_%d_1H'), currency)
        time.sleep(1)
