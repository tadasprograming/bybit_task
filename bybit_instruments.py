from pybit.unified_trading import HTTP
import time
from sqlalchemy import Column, Integer, String, BigInteger, Numeric
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd
import matplotlib.pyplot as plt


API_KEY = "EKim1rHsFKKuAKybhe"
API_SECRET = "XhEbHQpwNpUpoDIwFdG3YAzRdrzvp5oyBhob"

bybit_session = HTTP(
    api_key=API_KEY,
    api_secret=API_SECRET,
    testnet=True)

def get_data_from_bybit(function_name, **kwargs):
    if hasattr(bybit_session, function_name):
        api_function = getattr(bybit_session, function_name)
        return api_function(**kwargs)
    else:
        return print('Wrong function')

current_time = int(time.time() * 1000)
period = 24*60*60*1000

instruments_data = get_data_from_bybit('get_instruments_info', category="spot",
                                  symbol="BTCUSDT")
print(instruments_data)

instruments_db_engine = create_engine('sqlite:///instruments.db')

Base = declarative_base()


class Instruments(Base):
    __tablename__ = 'instruments'
    id = Column(Integer, primary_key=True)
    time = Column(BigInteger)
    symbol = Column(String)
    status = Column(String)
    minOrderQty = Column(Numeric)
    maxOrderQty = Column(Numeric)
    minOrderAmt = Column(Numeric)
    maxOrderAmt = Column(Numeric)
    tickSize = Column(Numeric)

    @classmethod
    def upload_data(cls, function_name, **kwargs):
        Session = sessionmaker(bind=instruments_db_engine)
        session = Session()

        data = get_data_from_bybit(function_name, **kwargs)

        instruments = cls(
         time=data['time'],
         symbol=data['result']['list'][0]['symbol'],
         status=data['result']['list'][0]['status'],
         minOrderQty=data['result']['list'][0]['lotSizeFilter']['minOrderQty'],
         maxOrderQty=data['result']['list'][0]['lotSizeFilter']['maxOrderQty'],
         minOrderAmt=data['result']['list'][0]['lotSizeFilter']['minOrderAmt'],
         maxOrderAmt=data['result']['list'][0]['lotSizeFilter']['maxOrderAmt'],
         tickSize=data['result']['list'][0]['priceFilter']['tickSize']
         )
        session.add(instruments)
        session.commit()


Base.metadata.create_all(instruments_db_engine)


'''for i in range(10):
    for symbol in ["BTCUSDT", "ETHUSDT"]:
        Instruments.upload_data('get_instruments_info', category="spot",
                                symbol=symbol)
    time.sleep(10)'''

with instruments_db_engine.connect() as conect:
    result = conect.execute(text(
        "SELECT time, minOrderAmt, maxOrderAmt FROM instruments WHERE symbol == 'BTCUSDT'"))
    rows = result.fetchall()


df = pd.DataFrame(rows, columns=['time', 'minOrderAmt', 'maxOrderAmt'])
df['time'] = pd.to_datetime(df['time']) 
df.plot(x='time', y=['minOrderAmt', 'maxOrderAmt'], kind='line')

plt.xlabel('Time')
plt.ylabel('Order Amount')
plt.title('Minimum and Maximum Order Amounts over Time')

plt.show()