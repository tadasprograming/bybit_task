from pybit.unified_trading import HTTP
from dataclasses import dataclass
import time
from decimal import Decimal
import pandas as pd
import mplfinance as mpf
from dataclasses_json import dataclass_json
import json


API_KEY = "EKim1rHsFKKuAKybhe"
API_SECRET = "XhEbHQpwNpUpoDIwFdG3YAzRdrzvp5oyBhob"

bybit_session = HTTP(
    api_key=API_KEY,
    api_secret=API_SECRET,
    testnet=True)


def get_data(category, symbol, interval, start, stop):
    kline_dic = bybit_session.get_kline(
        category=category,
        symbol=symbol,
        interval=interval,
        start=start,
        end=stop)
    return kline_dic['result']['list']

@dataclass_json
@dataclass
class KlineData:
    id: list[int]
    symbol: list[str]
    start_time: list[int]
    open_price: list[Decimal]
    high_price: list[Decimal]
    low_price: list[Decimal]
    close_price: list[Decimal]
    volume: list[Decimal]
    turnover: list[Decimal]

    @classmethod
    def load_from_json(cls, file_name):
        with open(file_name, 'r') as json_file:
            data_dict = json.load(json_file)
        return cls(
            id=data_dict['id'],
            symbol=data_dict['symbol'],
            start_time=[int(value) for value in data_dict['start_time']],
            open_price=[Decimal(value) for value in data_dict['open_price']],
            high_price=[Decimal(value) for value in data_dict['high_price']],
            low_price=[Decimal(value) for value in data_dict['low_price']],
            close_price=[Decimal(value) for value in data_dict['close_price']],
            volume=[Decimal(value) for value in data_dict['volume']],
            turnover=[Decimal(value) for value in data_dict['turnover']]
        )


current_time = int(time.time() * 1000)
period = 24*60*60*1000
kline_data = get_data(category="linear", symbol="BTCUSD",
                    interval=60,
                    start=current_time-period,
                    stop=current_time)

def parse_data(data, symbol='BTCUSD'):
    return KlineData(
        id=list(range(len(data))),
        symbol=[symbol for i in range(len(data))],
        start_time=[data[i][0] for i in range(len(data))],
        open_price=[Decimal(data[i][1]) for i in range(len(data))],
        high_price=[Decimal(data[i][2]) for i in range(len(data))],
        low_price=[Decimal(data[i][3]) for i in range(len(data))],
        close_price=[Decimal(data[i][4]) for i in range(len(data))],
        volume=[Decimal(data[i][5]) for i in range(len(data))],
        turnover=[Decimal(data[i][6]) for i in range(len(data))]
)


KlineDataclass = parse_data(kline_data)

def save_dataclass(Dataclass, file_name=str):
    dataclass_json_str = Dataclass.to_json()
    file_name = f'{file_name}.json'
    with open(file_name, 'w') as json_file:
        json_file.write(dataclass_json_str)


save_dataclass(KlineDataclass, 'BTCUSD_kline')
KlineDataclass = KlineData.load_from_json('BTCUSD_kline.json')


def plot_candlestick_chart():
    plot_data = {
        'date': KlineDataclass.start_time,
        'open': pd.to_numeric(KlineDataclass.open_price, errors='coerce'),
        'high': pd.to_numeric(KlineDataclass.high_price, errors='coerce'),
        'low': pd.to_numeric(KlineDataclass.low_price, errors='coerce'),
        'close': pd.to_numeric(KlineDataclass.close_price, errors='coerce'),
        'volume': pd.to_numeric(KlineDataclass.volume, errors='coerce')
    }

    df = pd.DataFrame(plot_data)
    df['date'] = pd.to_datetime(df['date'], unit='ms')
    df.set_index('date', inplace=True)

    # Plot the candlestick chart
    mpf.plot(df, type='candle', volume=True)


# Pasibandymui galima pabraižyt paskutinės dienos candlestick chart
plot_candlestick_chart()