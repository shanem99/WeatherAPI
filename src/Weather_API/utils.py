from datetime import datetime, timedelta
import time


def generate_hourly_epoch(date_str):
    """
    Generate epoch timestamps for every hour of a given day
    :param date_str: date string in the format "YYYY-MM-DD"
    :return: list of epoch timestamps
    """
    date = datetime.strptime(date_str, "%Y-%m-%d")
    timestamps = []

    for hour in range(24):
        dt = date + timedelta(hours=hour)
        epoch = int(time.mktime(dt.timetuple()))
        timestamps.append(epoch)

    return timestamps


async def query_weather_db(connection, cursor, city, date):
    """
    Query the weather database for weather data
    :param c: sqlite3 cursor
    :param city: city name
    :param date: date in the format "YYYY-MM-DD"
    :return: weather data
    """
    await cursor.execute(
        f"""
        SELECT * FROM weatherdata WHERE city = "{city}" AND date = "{date}"
    """
    )

    data = await cursor.fetchone()

    return data


async def insert_into_weather_db(connection, cursor, date, weather_dict, city):
    """
    Insert weather data into the database
    :param c: sqlite3 cursor
    :param city: city name
    :param date: date in the format "YYYY-MM-DD"
    :param avg_temp: average temperature
    :param min_temp: minimum temperature
    :param max_temp: maximum temperature
    :param avg_humidity: average humidity
    """
    await cursor.execute(
        f"""
        INSERT INTO weatherdata VALUES (
            "{date}",
            "{city}",
            {weather_dict["avg_temp"]},
            {weather_dict["min_temp"]},
            {weather_dict["max_temp"]},
            {weather_dict["avg_humidity"]}
        )
    """
    )

    await connection.commit()
