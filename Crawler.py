# https://binance-docs.github.io/apidocs/spot/cn/

import requests
import time
import datetime

BASE_URL="https://api.binance.com/"
PATH_CANDLESTICK_DATA = "api/v3/klines"
PATH_EXCHANGEINFO = "api/v3/exchangeInfo"
PATH_PRICE = "api/v3/ticker/price"


def is_multiple_of_k_minutes(k):
    now = datetime.datetime.now()
    minutes = now.hour * 60 + now.minute
    
    return minutes % k == 0

def current_finish_kline_time(k):
    now = datetime.datetime.now()

    while(now.minute % k != 0):
        now -= datetime.timedelta(minutes = 1)
    now -= datetime.timedelta(minutes = k)

    dt = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute)
    unix = int(dt.timestamp())
    print("Finish kline time = ", datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M'), "   unix = ", unix)
    
    return unix

def get_kline(symbol = "BTCUSDT", interval = "15m", startTime = str(current_finish_kline_time(15) * 1000), endTime = str(current_finish_kline_time(15) * 1000 + 1)):
    if (interval not in ["1s", "1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M"]):
        return 0

    # symbol = "BTCUSDT"
    # interval = "15m"  # 
    # startTime = str(current_finish_kline_time(15) * 1000)


    url = f"{BASE_URL}{PATH_CANDLESTICK_DATA}?symbol={symbol}&interval={interval}&startTime={startTime}&endTime={endTime}"
    # url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&startTime={startTime}&endTime={endTime}"
    # url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"

    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    
    
    print ("'''''''''''''''''''''''''''")
    print(f"Symbol = {symbol}")
    print(f"Interval = {interval}")
    print(f"StartTime = {datetime.datetime.fromtimestamp(int(startTime)/1000).strftime('%Y-%m-%d %H:%M')}")
    print(f"EndTime = {datetime.datetime.fromtimestamp(int(endTime)/1000).strftime('%Y-%m-%d %H:%M')}")
    print(f"Get '{len(response.json())}' Klines")
    print ("'''''''''''''''''''''''''''")

    print(response.json())

    return response.json()[0]


if __name__ == '__main__':
    l = get_kline()
    # print(type(int(float(l[1]))))

# [
#   [
#     1499040000000,      // k线开盘时间
#     "0.01634790",       // 开盘价
#     "0.80000000",       // 最高价
#     "0.01575800",       // 最低价
#     "0.01577100",       // 收盘价(当前K线未结束的即为最新价)
#     "148976.11427815",  // 成交量
#     1499644799999,      // k线收盘时间
#     "2434.19055334",    // 成交额
#     308,                // 成交笔数
#     "1756.87402397",    // 主动买入成交量
#     "28.46694368",      // 主动买入成交额
#     "17928899.62484339" // 请忽略该参数
#   ]
# ]