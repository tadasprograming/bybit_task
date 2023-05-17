from pybit.unified_trading import HTTP
import time
from sqlalchemy import Column, Integer, BigInteger, Float
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


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

kline_engine = create_engine('sqlite:///kline.db', echo=True)
Base = declarative_base()


class Kline(Base):
    __tablename__ = 'kline.db'
   
    id = Column(Integer, primary_key=True)
    start_time = Column(BigInteger)
    open_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    close_price = Column(Float)
    volume = Column(Float)
    turnover = Column(Float)


Base.metadata.create_all(kline_engine)