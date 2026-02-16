import json
import requests
from datetime import date
from pathlib import Path

DATA_FILE = Path("data/prices.json")
DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

URL = (
    "https://api.coingecko.com/api/v3/simple/price"
    "?ids=bitcoin,ethereum&vs_currencies=inr"
)

response = requests.get(URL, timeout=20)
response.raise_for_status()
prices = response.json()

today_data = {
    "date": str(date.today()),
    "BTC_INR": prices["bitcoin"]["inr"],
    "ETH_INR": prices["ethereum"]["inr"],
}

# Load previous data if exists
if DATA_FILE.exists():
    with open(DATA_FILE, "r") as f:
        old_data = json.load(f)
else:
    old_data = None

# Write only if data changed
if old_data != today_data:
    with open(DATA_FILE, "w") as f:
        json.dump(today_data, f, indent=2)
    print("Data changed. File updated.")
else:
    print("No change in prices. No update needed.")
