from fastapi import APIRouter, status, Depends
from Weather_API.data_interfaces.openweathermap import openWeather
from typing import Annotated, Union
from datetime import date
import Weather_API.utils as utils
from Weather_API.db.sqllite import get_db

router = APIRouter()


@router.get("/avg_daily_weather", status_code=status.HTTP_200_OK)
async def get_avg_daily_weather(
    city: Annotated[str, "City name"],
    state: Annotated[str, "State name"],
    date: Annotated[date, "Date in the format YYYY-MM-DD"],
    db=Depends(get_db),
) -> Union[dict, None]:

    connection, cursor = db

    db_data = await utils.query_weather_db(connection, cursor, city, date)

    if db_data:
        return {
            "date": db_data[0],
            "city": db_data[1],
            "avg_temp": db_data[2],
            "min_temp": db_data[3],
            "max_temp": db_data[4],
            "avg_humidity": db_data[5],
        }

    else:

        weather_data = openWeather().get_weather_data(
            city, state, date.strftime("%Y-%m-%d")
        )

        await utils.insert_into_weather_db(
            connection, cursor, date.strftime("%Y-%m-%d"), weather_data, city
        )

        if weather_data is None:
            return {"error": "No data found for the given city and state."}

        weather_data["date"] = date.strftime("%Y-%m-%d")
        weather_data["city"] = city

        return weather_data
