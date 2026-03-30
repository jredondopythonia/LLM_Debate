import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

resp = requests.get(
    "https://openrouter.ai/api/v1/models/user",
    headers={"Authorization": f"Bearer {api_key}"},
    timeout=20,
)
print(resp.status_code)
print(resp.json())