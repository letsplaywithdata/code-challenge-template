import pandas as pd


def get_weather_data(connection, station_id, date, page_id, page_size):
    # build the query based on the provided parameters
    query = "SELECT * FROM weather_data"

    if station_id and date:
        query += " WHERE station_id=%s AND date=%s"
        params = (station_id, date)
    elif station_id:
        query += " WHERE station_id=%s"
        params = (station_id,)
    elif date:
        query += " WHERE date=%s"
        params = (date,)
    else:
        params = ()

    query += " ORDER BY station_id, date"
    query += " LIMIT %s OFFSET %s"
    params += (page_size, (page_id - 1) * page_size)

    # execute the query and fetch the results
    with connection.connect() as conn:
        result = conn.execute(query, params).fetchall()

    # convert the results to a pandas dataframe and then to json
    df = pd.DataFrame(result, columns=['station_id', 'date', 'max_temp', 'min_temp', 'precipitation'])

    # convert the date column to datetime and format it as YYYY-MM-DD
    df['date'] = pd.to_datetime(df['date'], unit='ms').dt.strftime('%Y-%m-%d')

    return df.to_json(orient='records')


def get_weather_stats(connection, station_id, year, page_id, page_size):
    # build the query based on the provided parameters
    query = "SELECT station_id, year, avg_max_temp, avg_min_temp, avg_precipitation FROM weather_stats"

    if station_id and year:
        query += " WHERE station_id=%s AND year=%s"
        params = (station_id, year)
    elif station_id:
        query += " WHERE station_id=%s"
        params = (station_id,)
    elif year:
        query += " WHERE year=%s"
        params = (year,)
    else:
        params = ()

    query += " ORDER BY station_id, year"
    query += " LIMIT %s OFFSET %s"
    params += (page_size, (page_id - 1) * page_size)

    # execute the query and fetch the results
    with connection.connect() as conn:
        result = conn.execute(query, params).fetchall()

    # convert the results to a pandas dataframe and then to json
    df = pd.DataFrame(result, columns=['station_id', 'year', 'avg_max_temp', 'avg_min_temp', 'avg_precipitation'])

    return df.to_json(orient='records')