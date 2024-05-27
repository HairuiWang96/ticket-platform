# from nylas import Client


# nylas = Client(
#     api_key='nyk_v0_iFbclRKK47uPTGIDLA06QmnfW53Z4j8IkEI3eb6w969WKtLfibCeHTjJvSR3hFnW',
#     api_uri='https://api.eu.nylas.com'
# )


import os
from dotenv import load_dotenv
from nylas import Client

# Load environment variables from .env file
load_dotenv()

# Get Nylas API key and URL from environment variables
NYLAS_API_KEY = os.getenv('NYLAS_API_KEY')
NYLAS_API_URL = os.getenv('NYLAS_API_URL')

# Initialize Nylas Client with environment variables
nylas = Client(
    api_key=NYLAS_API_KEY,
    api_uri=NYLAS_API_URL
)