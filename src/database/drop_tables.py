# def drop_tables(conn):
#     cursor = conn.cursor()
#
#     # Drop weather data table
#     cursor.execute('''DROP TABLE IF EXISTS weather_data;''')
#     # Drop weather data logs table
#     cursor.execute('''DROP TABLE IF EXISTS weather_logs;''')
#     # Drop weather stats data table
#     cursor.execute('''DROP TABLE IF EXISTS weather_stats;''')
#
#     conn.commit()
#     cursor.close()

from sqlalchemy import MetaData, Table
from sqlalchemy.orm import declarative_base

from database.connection import engine

Base = declarative_base()
metadata = MetaData()

# Define tables to drop
weather_data = Table('weather_data', metadata, autoload=True, autoload_with=engine)
weather_logs = Table('weather_logs', metadata, autoload=True, autoload_with=engine)
weather_stats = Table('weather_stats', metadata, autoload=True, autoload_with=engine)

def drop_tables(engine):
    # Drop tables
    Base.metadata.drop_all(engine, [weather_data, weather_logs, weather_stats])
    print("Tables Dropped Successfully")





