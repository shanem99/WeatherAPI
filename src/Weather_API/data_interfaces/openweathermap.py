import requests
from Weather_API.utils import generate_hourly_epoch


class openWeather:
    def __init__(self) -> None:
        self.__api_key = "insert_your_api_key_here"

    def _get_city_coordinates(self, city: str, state: str):
        url = f"http://api.openweathermap.org/geo/1.0/direct"
        params = {"q": city, "appid": self.__api_key}
        response = requests.get(url, params=params)
        data = response.json()

        new_data = [
            {"lat": entry["lat"], "lon": entry["lon"]}
            for entry in data
            if entry["state"] == state
        ]

        if new_data == []:
            return None

        return new_data

    def _request_historical_weather_data(self, lat: float, lon: float, timestamp: int):
        url = "https://api.openweathermap.org/data/3.0/onecall/timemachine"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.__api_key,
            "dt": timestamp,
        }
        response = requests.get(url, params=params).json()["data"][0]
        return {key: response[key] for key in ("dt", "humidity", "temp")}

    def get_weather_data(self, city: str, state: str, date: str):
        coordinates = self._get_city_coordinates(city, state)
        if coordinates is None:
            return None

        timestamps = generate_hourly_epoch(date)

        data = []
        for timestamp in timestamps:
            for entry in coordinates:
                data.append(
                    self._request_historical_weather_data(
                        entry["lat"], entry["lon"], timestamp
                    )
                )

        return self.aggr_weather_data(data)

    def aggr_weather_data(self, data: list):
        if not data:
            return None

        avg_temp = sum(d["temp"] for d in data) / len(data)
        avg_humidity = sum(d["humidity"] for d in data) / len(data)
        min_temp = min(d["temp"] for d in data)
        max_temp = max(d["temp"] for d in data)

        return {
            "avg_temp": avg_temp,
            "avg_humidity": avg_humidity,
            "min_temp": min_temp,
            "max_temp": max_temp,
        }
