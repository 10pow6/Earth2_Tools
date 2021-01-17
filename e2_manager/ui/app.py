from flask import Flask, render_template, request
import requests
import json

import csv

from string import Template
from datetime import datetime

app = Flask(__name__)
BACKEND_API="http://localhost:8000/"

db_json_payload = """
    {
        "country_code": "$COUNTRY_CODE",
        "update_time": "$UPDATE_TIME",
        "trade_average": $TRADE_AVG,
        "final": $FINAL,
        "total_tiles_sold": $TOTAL_TILES_SOLD
    }
"""


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/manage')
def manage():
    return render_template('manage.html')

@app.route('/countries')
def countries():
    r = requests.get(BACKEND_API+"countries/db?skip=0&limit=400")

    return render_template('countries.html',country_data=r.json())

@app.route('/countries_export',methods = ['GET', 'POST'])
def countries_export():
    with open('ui_exports//countries.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)


        spamwriter.writerow( [ "country_code", "update_time", "trade_average", "final", "total_tiles_sold" ] )
        for country_row in request.json:
            spamwriter.writerow( [ country_row["country_code"], country_row["update_time"], country_row["trade_average"], country_row["final"], country_row["total_tiles_sold"] ] )

    return render_template('countries_export.html')   


@app.route('/countries_load_all', methods = ['GET', 'POST'])
def countries_load_all():
    #### TODO:  full country list to go here.  make 2-4 calls with a delay to api to be kind to E2 servers :P
    country_list = ["US","NU"]
    query_param = "?"

    for country in country_list:
        query_param += "c=" + country + "&"
    query_param = query_param[:-1]

    print("TRYING: " + BACKEND_API+"countries/e2" + query_param)
    status_codes = []
    r = requests.get(BACKEND_API+"countries/e2" + query_param)
    payload = r.json()["data"]["getTilePrices"]
    status_codes.append(r.status_code)

    cur_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]+"Z"
    for country in payload:
        country_payload = Template(db_json_payload).substitute(COUNTRY_CODE=country["countryCode"],UPDATE_TIME=cur_time,TRADE_AVG=country["tradeAverage"],FINAL=country["final"],TOTAL_TILES_SOLD=country["totalTilesSold"])
        r = requests.post(BACKEND_API+"countries/db", json=json.loads(country_payload) )
        status_codes.append(r.status_code)


    return render_template('countries_load_all.html',status_codes=status_codes)

