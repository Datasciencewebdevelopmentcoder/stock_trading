import requests
import openai
import os
import time
from dotenv import load_dotenv
import csv  # Import CSV module

load_dotenv()

PLOYGON_API_KEY = os.getenv("API_KEY")

url =f'https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&order=asc&limit=1000&sort=ticker&apiKey={PLOYGON_API_KEY}'


response = requests.get(url)
tickers = []
data = response.json()
print(data['next_url'])
for ticker in data['results']:
    tickers.append(ticker)

while 'next_url' in data:
    print("Fetching next page..."+data['next_url'])
    time.sleep(12)  # To respect rate limits
    response = requests.get(data['next_url'] + f'&apiKey={PLOYGON_API_KEY}')
    if response.status_code != 200:
        print(f"Error: Failed to fetch data. Status code: {response.status_code}")
        print(response.text)
        break
    data = response.json()
    if 'results' not in data:
        print("Unexpected response structure:", data)
        break
    for ticker in data['results']:
        tickers.append(ticker)

csv_headers = [
    'ticker', 'name', 'market', 'locale', 'primary_exchange', 'type', 'active',
    'currency_name', 'composite_figi', 'share_class_figi', 'last_updated_utc'
]

# Write the data to a CSV file
with open("tickers.csv", mode="w", newline="") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    writer.writeheader()  # Write the header row
    for ticker in tickers:
        row = {key: ticker.get(key, '') for key in csv_headers}
        writer.writerow(row)

print(f"Total tickers fetched: {len(tickers)}")
print("Tickers have been written to tickers.csv")
