import pandas as pd
from sqlalchemy import func, extract
from database.create_tables import WeatherStats, WeatherData


def calculate_weather_stats(session):
    # Query the weather stats
    weather_stats_query = session.query(
        WeatherData.station_id,
        extract('year', WeatherData.date).label('year'),
        func.avg(WeatherData.min_temp).label('avg_min_temp'),
        func.avg(WeatherData.max_temp).label('avg_max_temp'),
        func.avg(WeatherData.precipitation).label('avg_precipitation')
    ).group_by(
        WeatherData.station_id,
        extract('year', WeatherData.date)
    ).order_by(
        WeatherData.station_id,
        extract('year', WeatherData.date)
    )

    # Read the query results into a dataframe
    df = pd.read_sql(weather_stats_query.statement, session.bind)

    # Return the dataframe
    return df

