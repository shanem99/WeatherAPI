FROM python:3.10
WORKDIR /WeatherAPI
COPY . /WeatherAPI/
RUN pip install -r requirements.txt
EXPOSE 80
ENTRYPOINT [ "uvicorn", "src.Weather_API.server.main:app", "--host", "0.0.0.0", "--port", "80" ]