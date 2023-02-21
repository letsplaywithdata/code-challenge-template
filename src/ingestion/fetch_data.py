import os
from datetime import datetime
import pandas as pd
from database.create_tables import WeatherData, WeatherLogs
import numpy as np
from multiprocessing import Pool, cpu_count
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import QueuePool
from tqdm import tqdm
from multiprocessing import current_process


def process_file(file_path):
    """
    Helper function to process each file
    """
    print(f"Processing file: {file_path}")
    # Extract the station ID from the file name
    station_id = os.path.splitext(os.path.basename(file_path))[0]

    # Read the file into a dataframe
    file_data = pd.read_csv(file_path, sep='\t', header=None, names=['date', 'max_temp', 'min_temp', 'precipitation'])

    # Convert date column to datetime object
    file_data['date'] = pd.to_datetime(file_data['date'], format='%Y%m%d')

    # Replace -9999 with NaN
    file_data.replace(-9999, np.nan, inplace=True)

    # Convert temperature values from tenths of a degree Celsius to Celsius
    file_data['max_temp'] = file_data['max_temp'] / 10
    file_data['min_temp'] = file_data['min_temp'] / 10

    # Convert precipitation values from tenths of a millimeter to millimeters
    file_data['precipitation'] = file_data['precipitation'] / 10

    # Add station_id column to the dataframe
    file_data['station_id'] = station_id

    return file_data


def process_station_data(station_id, station_data, db_url):
    start_time = datetime.now()

    # Create a new engine and session for this process
    engine = create_engine(db_url, poolclass=QueuePool)
    session = sessionmaker(bind=engine)()

    # Check if any records from the file data already exist in the database for this station
    existing_records_df = pd.read_sql(
        session.query(WeatherData.date, WeatherData.station_id).filter_by(station_id=station_id).statement,
        session.bind)
    existing_records_df['date'] = pd.to_datetime(existing_records_df['date'], format='%Y-%m-%d')

    # Add only new records to the weather data DataFrame for this station
    new_records_df = station_data.merge(existing_records_df, how='left', on=['date', 'station_id'], indicator=True)
    new_records_df = new_records_df[new_records_df['_merge'] == 'left_only'].drop(columns=['_merge'])

    no_of_new_records = len(new_records_df.index)

    session.close()

    # Print the station ID and progress for this process
    progress = tqdm(total=1)
    progress.set_description(f"{current_process().name} processing station {station_id}")
    progress.update(1)
    progress.close()

    return {
        "station_id": station_id,
        "start_time": start_time,
        "end_time": datetime.now(),
        "no_of_records": no_of_new_records
    }


def fetch_data(data_dir, db_url):
    # Create database engine
    engine = create_engine(db_url, poolclass=QueuePool, max_overflow=0, pool_pre_ping=True)

    # Get a list of all weather data files
    files = [os.path.join(data_dir, file_name) for file_name in os.listdir(data_dir) if file_name.endswith(".txt")]

    # Use multiprocessing to process each file
    with Pool(4) as pool:
        file_data_list = pool.map(process_file, files)

    # Combine all file dataframes into a single dataframe
    weather_data_df = pd.concat(file_data_list)

    # Group the weather data by station ID
    station_groups = weather_data_df.groupby('station_id')

    # Process the data for each station in parallel
    with Pool(4) as pool:
        weather_log_rows = pool.starmap(process_station_data, [(station_id, station_data, db_url) for station_id, station_data in station_groups])

    # Convert list to DataFrame after loop has finished
    weather_log_row_df = pd.DataFrame(weather_log_rows)

    # Converting start_time and end_time to string format
    weather_log_row_df['start_time'] = weather_log_row_df['start_time'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
    weather_log_row_df['end_time'] = weather_log_row_df['end_time'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))

    # Dataframe outlook
    print(weather_data_df.head())
    print(weather_log_row_df.head())

    return weather_data_df, weather_log_row_df
