from api import server
from utils import adapter_method
from database import create_tables, drop_tables
from ingestion import fetch_data, ingest_data
from data_analysis import fetch_data_filters, weather_stats
from database.connection import Connection, db_creds
from database.create_tables import WeatherData, WeatherLogs, WeatherStats

if __name__ == "__main__":
    # Run mode input
    print(
        "Enter 1 to run only flask server. Enter 2 to reset and inject database database and then launch flask server")
    server_flag = input()
    # Create initial postgresql database adapters
    adapter_method.create_adapters()
    # Get connection to postgresql database
    with Connection() as conn:
        db_url = f"postgresql://{db_creds['PGUSER']}:{db_creds['PGPASSWORD']}@{db_creds['PGHOST']}/{db_creds['PGDATABASE']}"
        if server_flag == "2":
            # Drop the schemas if already present
            drop_tables.drop_tables(conn.engine)
            # Create required schemas
            create_tables.create_tables(conn.engine)

            # Weather station data folder
            weather_station_data = "../wx_data/"
            # Read weather station data from all input files
            print("Reading weather station data from input files")
            weather_df, weather_logs_df = fetch_data.fetch_data(weather_station_data, db_url)
            # Inject the weather data into database
            print("Uploading Weather data into database")
            ingest_data.upload_data(WeatherData, weather_df, conn.session)
            # Inject the weather stations logs into database
            print("Uploading Weather logs into database")
            ingest_data.upload_data(WeatherLogs, weather_logs_df, conn.session)

            # Fetch weather stats data from database
            print("Fetching Weather Stats data")
            weather_stats_df = weather_stats.calculate_weather_stats(conn.session)
            print(weather_stats_df.head())

            # Insert weather stats data into database
            print("Uploading Weather stats into database")
            ingest_data.upload_data(WeatherStats, weather_stats_df, conn.session)

            # start flask server
            server.start_server(conn)

        if server_flag == "1":
            # Start Flask Server
            server.start_server(conn)

        # Close DB connection
        conn.session.close()
        conn.engine.dispose()
