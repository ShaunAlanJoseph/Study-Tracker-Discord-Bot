from os import getenv
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = getenv("API_TOKEN") or ""
ADMIN_CHANNEL_ID = int(getenv("ADMIN_CHANNEL_ID") or 0)