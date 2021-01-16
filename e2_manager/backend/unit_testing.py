import requests
import json
from string import Template
from datetime import datetime


def run_query(payload, endpoint, session_id = None): # A simple function to use requests.post to make the API call. Note the json= section.
    cookies = {}
    if session_id is not None:
        cookies = {'sessionid': session_id }

    request = requests.post(endpoint, json=payload, cookies=cookies)

    if request.status_code == 200:
        response = request.json()
        return response
    else:
        return '{ "errors": [{ "status": "-1", "detail": "' + format(request.status_code, payload) + '"}]}'


db_json_payload = """
    {
        "country_code": "$COUNTRY_CODE",
        "update_time": "$UPDATE_TIME",
        "trade_average": $TRADE_AVG,
        "final": $FINAL,
        "total_tiles_sold": $TOTAL_TILES_SOLD
    }
"""


# Hello World!
print("==Hello World==")
r = requests.get('http://localhost:8000/')
print(r.text)

# Get E2 Countries
r = requests.get('http://localhost:8000/countries/e2?c=US&c=NU')
store_dbs = r.json()
print("==E2 Countries==")
print(r.json())

# Get DB Countries
print("==Current DB Countries Prior Load==")
r = requests.get('http://localhost:8000/countries/db?skip=0&limit=1000')
print(r.json())


# Write E2 Results to DB
cur_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]+"Z"
for country in store_dbs["data"]["getTilePrices"]:
    payload = Template(db_json_payload).substitute(COUNTRY_CODE=country["countryCode"],UPDATE_TIME=cur_time,TRADE_AVG=country["tradeAverage"],FINAL=country["final"],TOTAL_TILES_SOLD=country["totalTilesSold"])
    response = run_query(json.loads(payload), 'http://localhost:8000/countries/db')


# Get DB Countries
print("==Current DB Countries After Load==")
r = requests.get('http://localhost:8000/countries/db?skip=0&limit=1000')
print(r.json())

# Get Specific DB Countries
print("==Get just US==")
r = requests.get('http://localhost:8000/countries/db?country_code=US')
print(r.json())