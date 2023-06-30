# https://binance-docs.github.io/apidocs/spot/cn/

import requests
import time
import datetime
import logging

# create logger, then setLevel
allLogger = logging.getLogger('allLogger')
allLogger.setLevel(logging.DEBUG)

#create stream handler
streamHandler = logging.StreamHandler()
streamHandler.setLevel(logging.DEBUG)

def Time_UTC8(sec):
    if time.strftime('%z') == "+0800":
        return datetime.datetime.now().timetuple()
    return (datetime.datetime.now() + datetime.timedelta(hours=8)).timetuple()
# create formatter, then handler setFormatter
AllFormatter = logging.Formatter("%(asctime)s - [%(filename)s line:%(lineno)d] - %(levelname)s: %(message)s")
AllFormatter.converter = Time_UTC8
streamHandler.setFormatter(AllFormatter)

# logger addHandler
allLogger.addHandler(streamHandler)




def Send_message_to_user(Message):
    url = 'http://localhost:5000/Send_Message'
    obj = {'Message': Message,
            'Chat_ID': "998618031"}
    
    x = requests.post(url, data = obj)

    print(x.text)


def is_multiple_of_k_minutes(k):
    now = datetime.datetime.now()
    minutes = now.hour * 60 + now.minute
    
    return minutes % k == 0

def current_finish_kline_time(time_frame, n_bar):
    # UTC => 因為是GCP的環境，不同的環境這邊吃到的可能會不相同
    # 不能修改，因為 Binance 那邊吃的時間是 UTC
    now = datetime.datetime.now() 
          
    while(now.minute % time_frame != 0):
        now -= datetime.timedelta(minutes = 1)
    # now -= datetime.timedelta(minutes = (time_frame))
    start = now - datetime.timedelta(minutes = (time_frame*n_bar))
    end = now - datetime.timedelta(minutes = (time_frame)) + datetime.timedelta(seconds=1)


    start_dt = datetime.datetime(start.year, start.month, start.day, start.hour, start.minute)
    end_dt = datetime.datetime(end.year, end.month, end.day, end.hour, end.minute)
    
    start_unix = int(start_dt.timestamp())
    end_unix = int(end_dt.timestamp())
    # print(f"Finish kline time = {datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M')}, unix = {unix}")
    
    return start_unix, end_unix

def get_kline(symbol = None, interval = None, n=1):
    BASE_URL="https://api.binance.com/"
    PATH_CANDLESTICK_DATA = "api/v3/klines"
    PATH_EXCHANGEINFO = "api/v3/exchangeInfo"
    PATH_PRICE = "api/v3/ticker/price"
    interval_cases = {
        '1m': 1,
        '3m': 3,
        '5m': 5,
        '15m': 15,
        '30m': 30,
        '1h': 60,
        '2h': 120,
        '4h': 240,
        '6h': 360,
        '8h': 480,
        '12h': 720,
        '1d': 1440,
        '3d': 4320,
        "1w": 10080,
        "1M": 43200 # 30 days
    }
    k_time = interval_cases.get(interval, 0)
    
    if k_time == 0: 
        allLogger.error(f"Invalid interval. Your 'interval' is '{interval}'")
        raise ValueError("Invalid interval.")
    if symbol == None:  
        allLogger.error(f"Invalid symbol. Your 'symbol' is None")
        raise ValueError("Invalid symbol.") 
    # if startTime == None:   startTime = str(current_finish_kline_time(time_frame=15) * 1000)
    # if endTime == None: endTime = str((current_finish_kline_time(time_frame=15) + 1) * 1000)

    startTime, endTime = current_finish_kline_time(time_frame=15, n_bar=n)
    startTime = str(startTime * 1000)
    endTime = str(endTime * 1000)

# ====================================================================================================


    url = f"{BASE_URL}{PATH_CANDLESTICK_DATA}?symbol={symbol}&interval={interval}&startTime={startTime}&endTime={endTime}"
    # url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&startTime={startTime}&endTime={endTime}"
    # url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"

    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    
    

    allLogger.info("================== K Lines Info ==================")
    allLogger.info(f"Symbol = {symbol}")
    allLogger.info(f"Interval = {interval}")
    allLogger.info(f"Start Time = {datetime.datetime.fromtimestamp((int(startTime)/1000)+28800).strftime('%Y-%m-%d %H:%M')}")
    allLogger.info(f"End Time = {datetime.datetime.fromtimestamp((int(endTime)/1000)+28800).strftime('%Y-%m-%d %H:%M')}")
    allLogger.info(f"Get '{len(response.json())}' k bars")
    # allLogger.info(response.json())
    allLogger.info("==================================================")


    return response.json()[0]


if __name__ == '__main__':
    l = get_kline(symbol = "BTCUSDT", interval = "15m")
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