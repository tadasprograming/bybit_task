from pybit.unified_trading import HTTP
import time

API_KEY = "EKim1rHsFKKuAKybhe"
API_SECRET = "XhEbHQpwNpUpoDIwFdG3YAzRdrzvp5oyBhob"

session = HTTP(
    api_key=API_KEY,
    api_secret=API_SECRET,
    testnet=False
    )

current_time = int(time.time() * 1000)
period = 24*60*60*1000  # para

kline_dic = session.get_kline(
    category="linear",
    symbol="BTCUSD",
    interval=60,
    start=current_time-period,
    end=current_time
)  # paskutinės paros data

print(len(kline_dic["result"]["list"]))