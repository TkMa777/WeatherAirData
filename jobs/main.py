import asyncio
import re

from aiokafka import AIOKafkaProducer
import os
import json
import logging

from jobs.air_quality_api import fetch_air_quality_data, air_api_key
from jobs.weather_api import fetch_openweather_data, weather_api_key

# Configuration de la logging
logging.basicConfig(level=logging.INFO)

# Variables d'environnement
KAFKA_BOOTSTRAP_SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVER", "localhost:9092")
WEATHER_TOPIC = os.getenv("WEATHER_TOPIC", "weather_data")
QUALITY_TOPIC = os.getenv("QUALITY_TOPIC", "quality_data")

city_codes = {
    'Paris': '@5722',
    'Lyon': '@3028',
    'Marseille': '@14082',
    'Toulouse': '@3828',
    'Nice': '@6887'
}


def get_iaqi_value(aqi_data, key):
    # On recoit tout les données de l'iaqi, return None si y a pas de valeur
    try:
        return aqi_data['data']['iaqi'][key]['v']
    except KeyError:
        return None


def format_data_quality(aqi_data):
    try:
        def extract_city_name(full_name):
            if "Promenade Des Anglais" in full_name:
                return "Nice"
            match = re.match(r"([A-Za-z]+)[_, ]", full_name)
            if match:
                return match.group(1)
            return full_name

        city_name = extract_city_name(aqi_data['data']['city']['name'])

        cities = [
            "Lyon Centre, France",
            "Marseille_PlaceVerneuil, PACA, Franc",
            "Toulouse Berthelot, France",
            "Promenade Des Anglais, PACA, France"
        ]

        extracted_cities = [extract_city_name(city) for city in cities]
        print(extracted_cities)

        formatted_data = {
            'status': aqi_data['status'],
            'aqi': aqi_data['data']['aqi'],
            'idx': aqi_data['data']['idx'],
            'attribution1_url': aqi_data['data']['attributions'][0]['url'],
            'attribution1_name': aqi_data['data']['attributions'][0]['name'],
            'attribution2_url': aqi_data['data']['attributions'][1]['url'],
            'attribution2_name': aqi_data['data']['attributions'][1]['name'],
            'city_geo_lat': aqi_data['data']['city']['geo'][0],
            'city_geo_lon': aqi_data['data']['city']['geo'][1],
            'city_name': city_name,
            'city_url': aqi_data['data']['city']['url'],
            'dew_value': get_iaqi_value(aqi_data, 'dew'),
            'co_value': get_iaqi_value(aqi_data, 'co'),
            'h_value': get_iaqi_value(aqi_data, 'h'),
            'no2_value': get_iaqi_value(aqi_data, 'no2'),
            'so2_value': get_iaqi_value(aqi_data, 'so2'),
            'o3_value': get_iaqi_value(aqi_data, 'o3'),
            'p_value': get_iaqi_value(aqi_data, 'p'),
            'pm10_value': get_iaqi_value(aqi_data, 'pm10'),
            'pm25_value': get_iaqi_value(aqi_data, 'pm25'),
            't_value': get_iaqi_value(aqi_data, 't'),
            'w_value': get_iaqi_value(aqi_data, 'w'),
            'wg_value': get_iaqi_value(aqi_data, 'wg'),
            'time_s': aqi_data['data']['time']['s'],
            'time_tz': aqi_data['data']['time']['tz'],
            'time_v': aqi_data['data']['time']['v'],
            'time_iso': aqi_data['data']['time']['iso'],
            'debug_sync': aqi_data['data']['debug']['sync']
        }
        return formatted_data
    except KeyError as e:
        print(f"Missing data for key: {e}")
        return None


def format_data_weather(raw_data):
    # Convertir temp en Celsius
    temp_celsius = raw_data['main']['temp'] - 273.15
    feels_like_celsius = raw_data['main']['feels_like'] - 273.15
    temp_min_celsius = raw_data['main']['temp_min'] - 273.15
    temp_max_celsius = raw_data['main']['temp_max'] - 273.15

    # On fait split pour laisser que des villes.
    city_name = raw_data['name']
    if 'Arrondissement de' in city_name:
        city_name = city_name.split(' ')[2]
    elif 'District of' in city_name:
        city_name = city_name.replace('District of ', '')

    formatted_data = {
        'lon': raw_data['coord']['lon'],
        'lat': raw_data['coord']['lat'],
        'weather_id': raw_data['weather'][0]['id'],
        'main': raw_data['weather'][0]['main'],
        'description': raw_data['weather'][0]['description'],
        'icon': raw_data['weather'][0]['icon'],
        'temp': temp_celsius,
        'feels_like': feels_like_celsius,
        'temp_min': temp_min_celsius,
        'temp_max': temp_max_celsius,
        'pressure': raw_data['main']['pressure'],
        'humidity': raw_data['main']['humidity'],
        'visibility': raw_data.get('visibility', 10000),
        'wind_speed': raw_data['wind']['speed'],
        'wind_deg': raw_data['wind']['deg'],
        'clouds_all': raw_data['clouds']['all'],
        'country': raw_data['sys']['country'],
        'sunrise': raw_data['sys']['sunrise'],
        'sunset': raw_data['sys']['sunset'],
        'timezone': raw_data['timezone'],
        'city_id': raw_data['id'],
        'city_name': city_name,
        'cod': raw_data['cod']
    }
    return formatted_data


async def main():
    # Fonction asynchrone de base pour envoyer des données weather et air à Kafka
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVER)
    await producer.start()
    try:
        while True:
            for city, code in city_codes.items():
                # WEATHER
                raw_weather_data = await fetch_openweather_data(city, weather_api_key)
                if raw_weather_data:
                    formatted_weather_data = format_data_weather(raw_weather_data)
                    logging.info("Formatted Weather Data for %s: %s", city, formatted_weather_data)
                    weather_message = json.dumps(formatted_weather_data).encode('utf-8')
                    await producer.send_and_wait(WEATHER_TOPIC, value=weather_message, key=city.encode())
                else:
                    logging.error("Failed to fetch weather data for %s.", city)

                # AIR_QUALITY
                raw_quality_data = await fetch_air_quality_data(code, air_api_key)
                if raw_quality_data:
                    formatted_quality_data = format_data_quality(raw_quality_data)
                    logging.info("Formatted Air Quality Data for %s: %s", city, formatted_quality_data)
                    quality_message = json.dumps(formatted_quality_data).encode('utf-8')
                    await producer.send_and_wait(QUALITY_TOPIC, value=quality_message, key=city.encode())
                else:
                    logging.error("Failed to fetch air quality data for %s.", city)

            await asyncio.sleep(20)
    finally:
        await producer.stop()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Program stopped by user")
