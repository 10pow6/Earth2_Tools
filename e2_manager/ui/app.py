from flask import Flask, render_template, request
import requests
import json

import csv

from string import Template
from datetime import datetime

app = Flask(__name__)
BACKEND_API="http://localhost:8000/"

# To Be Implemented
E2_RATE_LIMITER=1


db_json_payload = """
    {
        "country_code": "$COUNTRY_CODE",
        "update_time": "$UPDATE_TIME",
        "trade_average": $TRADE_AVG,
        "final": $FINAL,
        "total_tiles_sold": $TOTAL_TILES_SOLD
    }
"""

db_json_property_payload = """
    {
        "landfield_id": "$LANDFIELD_ID",
        "for_sale": $FOR_SALE,
        "description": "$DESCRIPTION",
        "location": "$LOCATION",
        "center": "$CENTER",
        "price": $PRICE,
        "country": "$COUNTRY",
        "tile_count": $TILE_COUNT,
        "current_value": $CURRENT_VALUE,
        "trading_value": $TRADING_VALUE,
        "tile_class": $TILE_CLASS,
        "update_time": "$UPDATE_TIME",
        "profile_id": "$PROFILE_ID"
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

@app.route('/countries_detail/<string:country_code>')
def countries_detail(country_code):
    r = requests.get(BACKEND_API+"countries_historical/db?country_code=" + country_code)

    return render_template('countries_detail.html',country_data=r.json(), country_code=country_code)


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




@app.route('/properties_load/<string:profile_id>', methods = ['GET', 'POST'])
def properties_load(profile_id):
    query_param = "?profile_id=" + profile_id
    print("TRYING: " + BACKEND_API+"properties_count/e2/" + query_param)

    status_codes = []
    r = requests.get(BACKEND_API+"properties_count/e2/" + query_param)
    total_props = r.json()["data"]["getUserLandfields"]["count"]
    print("TOTAL_PROPS: " + str(total_props) )
    status_codes.append(r.status_code)

    pages = 1
    if( total_props / 60 > total_props // 60 ):
        pages = total_props//60 + 1
    else:
        pages = total_props//60

    cur_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]+"Z"
    for i in range(1,(pages+1) ):
        query_page =  query_param + "&page=" + str(i) + "&count=60"
        
        r = requests.get(BACKEND_API+"properties/e2" + query_page)
        status_codes.append(r.status_code)


        payloads = r.json()["data"]["getUserLandfields"]["landfields"]
        
        final_property_json_str = []
        for property_payload in payloads:
            prop = Template(db_json_property_payload).substitute(
                LANDFIELD_ID=property_payload["id"],
                FOR_SALE=str(property_payload["forSale"]).lower(),
                DESCRIPTION=property_payload["description"],
                LOCATION=property_payload["location"],
                CENTER=property_payload["center"],
                PRICE=property_payload["price"],
                COUNTRY=property_payload["country"],
                TILE_COUNT=property_payload["tileCount"],
                CURRENT_VALUE=property_payload["currentValue"],
                TRADING_VALUE=property_payload["tradingValue"],
                TILE_CLASS=property_payload["tileClass"],
                UPDATE_TIME=cur_time,
                PROFILE_ID=profile_id )
            
            final_property_json_str.append(prop)
        
        final_property_json = '[' + ','.join(final_property_json_str) + ']'
        print(final_property_json)
  
        r = requests.post(BACKEND_API+"properties/db", json=json.loads(final_property_json) )
        status_codes.append(r.status_code)
        

        

    return render_template('properties_load.html',status_codes=status_codes)