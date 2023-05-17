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


Base.metadata.create_all(kline_engine)

current_time = int(time.time() * 1000)
period = 24*60*60*1000  # para

def save_data_to_db(symbol, interval, start, stop):
    Session = sessionmaker(bind=kline_engine)
    session = Session()

    kline_dic = bybit_session.get_kline(
        category="linear",
        symbol=symbol,
        interval=interval,
        start=start,
        end=stop
        )
    
    for list in kline_dic["result"]["list"]:
        kline = Kline(
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


save_data_to_db(symbol="BTCUSD", interval=60, start=current_time-period,
                stop=current_time)