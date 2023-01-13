import requests
import time
import telegram
mexc_url = "https://contract.mexc.com/api/v1/contract/ticker"
bingX_url = "https://api-swap-rest.bingbon.pro/api/v1/market/getTicker"
binance_url = "https://fapi.binance.com/fapi/v1/ticker/price"


chat_token = "5963692938:AAEPEQRG5rME9HYUD5NNMgK4pNDbKFL97oQ"
bot = telegram.Bot(token=chat_token)

symbol = "ROSE"
bot_url = f"https://api.telegram.org/bot{chat_token}/sendMessage?"


def mexc_request_data(url) -> None:
    params = {"symbol": symbol+"_USDT"}
    data = requests.get(url, params=params)
    data = data.json()
    return data


def bingX_request_data(url) -> None:
    params = {"symbol": symbol+"-USDT"}
    data = requests.get(url, params=params)
    data = data.json()
    return data


def binance_request_data(url) -> None:
    params = {"symbol": symbol+"USDT"}
    data = requests.get(url, params=params)
    data = data.json()
    return data


count = 0
Done = False
while not Done:
    try:
        bingX_data = bingX_request_data(bingX_url)
        mexc_data = mexc_request_data(mexc_url)
        binance_data = binance_request_data(binance_url)["price"]

        bingX_price = (bingX_data["data"]["tickers"][0])
        mexc_bid1 = mexc_data["data"]["bid1"]  # 매수 1 호가
        mexc_ask1 = mexc_data["data"]["ask1"]  # 매도 1 호가
        bingX_bid1 = float(bingX_data["data"]["tickers"]
                           [0]["bidPrice"])  # 빙엑 매수 1호가
        bingX_ask1 = float(
            (bingX_data["data"]["tickers"][0]["askPrice"]))  # 빙엑 매도 1호가
        if bingX_ask1 > mexc_bid1:
            gap = round(bingX_ask1/mexc_ask1 * 100 - 100, 3)
            print("bing", gap, count)
            if gap > 0.5:
                text = f'''
ROSEgap : {gap}%

bingX : {bingX_ask1}
mexc : {mexc_bid1}
binance : {binance_data}
              '''
                print(text)
                data = {"chat_id": "-1001895027074", "text": text}
                res = requests.post(bot_url, json=data)

        elif mexc_bid1 >= bingX_ask1:
            gap = round(mexc_bid1 / bingX_ask1 * 100 - 100, 3) * -1
            print("mexc", gap, count)
            text = f'''
역갭발생
ROSEgap : {gap}%

bingX : {bingX_ask1}
mexc : {mexc_bid1}
binance : {binance_data}
              '''
            print(text)
            data = {"chat_id": "-1001895027074", "text": text}
            res = requests.post(bot_url, json=data)
        time.sleep(5)
    except Exception as e:
        data = {"chat_id": "5792701026", "text": f"오류발생 : {e}"}
        res = requests.post(bot_url, json=data)
        time.sleep(3)
