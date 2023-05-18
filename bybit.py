from pybit.unified_trading import HTTP
import time
from sqlalchemy import Column, Integer, BigInteger, Float, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


API_KEY = "EKim1rHsFKKuAKybhe"
API_SECRET = "XhEbHQpwNpUpoDIwFdG3YAzRdrzvp5oyBhob"

bybit_session = HTTP(
    api_key=API_KEY,
    api_secret=API_SECRET,
    testnet=True
    )


class kline():
    def __init__(self, category, symbol):
        self.category = category
        self.symbol = symbol

    def get_data(self, interval, start, stop):
        self.interval = interval
        self.start = start
        self.stop = stop
        self.kline_dic = bybit_session.get_kline(
            category=self.category,
            symbol=self.symbol,
            interval=self.interval,
            start=self.start,
            end=self.stop)
        if self.kline_dic['retMsg'] == 'OK':
            self.kline_data = self.kline_dic['result']['list']
            return self.kline_data
        else:
            return print('Failed to get data from API')
        
    def plot_data(self)
    
current_time = int(time.time() * 1000)
period = 24*60*60*1000  # para

kline_BTCUSD = kline(category="linear", symbol="BTCUSD")
print(kline_BTCUSD.get_data(interval=60,start=current_time-period,
                            stop=current_time))
    

kline_engine = create_engine('sqlite:///kline.db', echo=True)

Base = declarative_base()


class Kline(Base):
    __tablename__ = 'kline'
    id = Column(Integer, primary_key=True)
    symbol = Column(String)
    start_time = Column(BigInteger)
    open_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    close_price = Column(Float)
    volume = Column(Float)
    turnover = Column(Float)

    @classmethod
    def upload_data(cls, category, symbol, interval, start, stop):
        Session = sessionmaker(bind=kline_engine)
        session = Session()

        kline_dic = bybit_session.get_kline(
            category=category,
            symbol=symbol,
            interval=interval,
            start=start,
            end=stop
        )

        for list in kline_dic["result"]["list"]:
            kline = cls(
                symbol=symbol,
                start_time=list[0],
                open_price=list[1],
                high_price=list[2],
                low_price=list[3],
                close_price=list[4],
                volume=list[5],
                turnover=list[6]
            )
            session.add(kline)
            session.commit()


Base.metadata.create_all(kline_engine)




Kline.upload_data(category="linear", symbol="BTCUSD", interval=60,
                  start=current_time-period, stop=current_time)
