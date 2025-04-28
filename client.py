import requests

API_URL = ("http://34.58.157.204:5000/api/time?city=London")  # <-- replace with your actual IP
TOKEN = "supersecrettoken123"

headers = {
    "Authorization": f"Bearer {TOKEN}"
}

try:
    response = requests.get(API_URL, headers=headers)
    if response.status_code == 200:
        print("Success:", response.json())
    else:
        print("Failed:", response.status_code, response.text)
except Exception as e:
    print("Error connecting to API:", e)
