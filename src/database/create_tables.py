from sqlalchemy import Column, Integer, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class WeatherData(Base):
    __tablename__ = 'weather_data'

    station_id = Column(String(20), primary_key=True)
    date = Column(Date, primary_key=True)
    max_temp = Column(Numeric)
    min_temp = Column(Numeric)
    precipitation = Column(Numeric)


class WeatherLogs(Base):
    __tablename__ = 'weather_logs'

    start_time = Column(Date)
    end_time = Column(Date)
    no_of_records = Column(Integer)
    station_id = Column(String(20), primary_key=True)


class WeatherStats(Base):
    __tablename__ = 'weather_stats'

    station_id = Column(String(20), primary_key=True)
    year = Column(Integer, primary_key=True)
    avg_min_temp = Column(Numeric)
    avg_max_temp = Column(Numeric)
    avg_precipitation = Column(Numeric)


def create_tables(engine):
    Base.metadata.create_all(engine)
    print("Created Tables Successfully")
