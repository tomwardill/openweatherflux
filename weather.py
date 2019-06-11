import json

import influxdb
import requests

config = json.load(open('config.json'))


def get_weather():
    response = requests.get(
        config['WEATHER_URL'],
        params={
            'id': config['CITY_ID'],
            'appid': config['API_KEY'],
            'units': 'metric'
        }
    )
    json_resp = response.json()
    result = {
        'rain': float(json_resp.get('rain', {'1h': 0.0}).get('1h')),
        'wind': float(json_resp.get('wind', {'speed': 0.0}).get('speed')),
        'temp': float(json_resp.get('main', {'temp': 0.0}).get('temp')),
        'humidity': float(json_resp.get('main', {'humidity': 0.0}).get('humidity'))
    }
    return result


def post_weather(weather):
    client = influxdb.InfluxDBClient(
        config['INFLUX_HOST'], 8086, database='weather')
    points = []
    for measurement, value in weather.items():
        point = {
            'measurement': measurement,
            'fields': {'value': value}
        }
        points.append(point)
    client.write_points(points)


if __name__ == "__main__":
    weather = get_weather()
    post_weather(weather)
