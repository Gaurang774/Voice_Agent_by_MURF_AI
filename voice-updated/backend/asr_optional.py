import os
import requests
# below code is to check which models does my api key support
API_KEY = os.getenv("OPENROUTER_API_KEY")  # or set it directly as a string
URL = "https://openrouter.ai/api/v1/models"  # endpoint to list models

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

response = requests.get(URL, headers=headers)
response.raise_for_status()

models = response.json().get("data", [])
print("Available models:")
for m in models:
    print("-", m.get("id"), "|", m.get("name"))

