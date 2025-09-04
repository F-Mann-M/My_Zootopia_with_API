import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")
API_URL = "https://api.api-ninjas.com/v1/animals?"


def fetch_data_from_api(animal_name):
    """
    takes in an animal name,
    sends a query to animal api,
    gets json as response,
    returns list of dicts
    """

    response = requests.get(API_URL, params={"name": animal_name}, headers={"X-Api-Key": API_KEY})
    response = response.json()

    return response