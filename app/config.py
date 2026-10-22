from dotenv import load_dotenv
import os

load_dotenv()

TG_TOKEN = os.getenv("TG_TOKEN")
TG_CHAT_ID = os.getenv("TG_CHAT_ID")

URL = [url.strip() for url in os.getenv("URL").split(",") if url.strip()]

CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "30"))
REQ_TIMEOUT = int(os.getenv("REQ_TIMEOUT", "10"))
