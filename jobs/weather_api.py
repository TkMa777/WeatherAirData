from fastapi import FastAPI
import httpx

app = FastAPI()

weather_api_key = "votre_api_key"


async def fetch_openweather_data(city, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return {"error": "Failed to fetch data from OpenWeatherMap", "statusCode": response.status_code}
