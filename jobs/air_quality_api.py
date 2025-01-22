import logging
from fastapi import FastAPI
import httpx

app = FastAPI()

air_api_key = "votre_api_key"


async def fetch_air_quality_data(city_key, api_key):
    url = f"https://api.waqi.info/feed/{city_key}/?token={api_key}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            logging.error("Failed: " + str(response.status_code))
            return None
