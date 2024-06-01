from nylas import Client
import os
from dotenv import load_dotenv

load_dotenv()

nylas = Client(
    api_key = os.environ.get("NYLAS_API_KEY"),
    api_uri = os.environ.get("NYLAS_API_URI"),
)