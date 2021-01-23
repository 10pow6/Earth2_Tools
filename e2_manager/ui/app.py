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
        "tile_class_revenue": $TILE_CLASS_REVENUE,
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

@app.route('/properties/', defaults={'profile_id': None})
@app.route('/properties/<string:profile_id>',methods=['GET'])
def properties(profile_id=None):

    skip  = request.args.get('skip', None, type=int)

    limit  = 10
    total  = request.args.get('total', None, type=int)
    if( skip == None ):
        skip = 0
    else:
        skip = skip * limit

    if( profile_id != None and total == None ):
        total = requests.get(BACKEND_API+"properties_profile_id_count/db/?profile_id="+profile_id).text
    else:
        total = total
    
    print("SKIP: ", skip)
    print("LIMIT: ", limit)
    print("TOTAL: ", total)
    print("PROFILE_ID: ", profile_id)

    r = requests.get(BACKEND_API+"properties_profile_id/db/")

    q = None

    if( profile_id != None ):
        q = requests.get(BACKEND_API+"properties_by_id/db/?skip=" + str(skip) + "&limit=" + str(limit) + "&profile_id=" + profile_id).json()
    else:
        q = json.loads("{}")

    return render_template('properties.html',all_profile_id=r.json(), property_data=q, profile_id=profile_id, skip=skip, limit=limit,total=total)




@app.route('/countries_detail/<string:country_code>')
def countries_detail(country_code):
    r = requests.get(BACKEND_API+"countries_historical/db?country_code=" + country_code)
    print(r.json())
    return render_template('countries_detail.html',country_data=r.json(), country_code=country_code)


@app.route('/countries_export',methods = ['GET', 'POST'])
def countries_export():
    with open('ui_exports//countries.csv', 'w', newline='',encoding='utf-8') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)


        spamwriter.writerow( [ "country_code", "update_time", "trade_average", "final", "total_tiles_sold" ] )
        for country_row in request.json:
            spamwriter.writerow( [ country_row["country_code"], country_row["update_time"], country_row["trade_average"], country_row["final"], country_row["total_tiles_sold"] ] )

    return render_template('countries_export.html')   



#### TODO:  parameterize this to accept string list
@app.route('/countries_load_all', methods = ['GET', 'POST'])
def countries_load_all():
    print("TRYING: " + BACKEND_API+"countries_all/e2")
    status_codes = []
    r = requests.get(BACKEND_API+"countries_all/e2")

    cur_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]+"Z"
    for payload in r.json():
        country_payload = payload["data"]["getTilePrices"]
        status_codes.append(r.status_code)
        for country in country_payload:
            db_payload = Template(db_json_payload).substitute(COUNTRY_CODE=country["countryCode"],UPDATE_TIME=cur_time,TRADE_AVG=country["tradeAverage"],FINAL=country["final"],TOTAL_TILES_SOLD=country["totalTilesSold"])
            r = requests.post(BACKEND_API+"countries/db", json=json.loads(db_payload) )
            status_codes.append(r.status_code)


    return render_template('countries_load_all.html',status_codes=status_codes)

#### TODO:  parameterize this to accept string list
@app.route('/countries_load_subset', methods = ['GET', 'POST'])
def countries_load_subset():

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



@app.route('/properties_export',methods = ['GET', 'POST'])
def properties_export():

    r = requests.get(BACKEND_API+"properties_by_id/db/?skip=0&limit=" + str(request.json["total_props"]) + "&profile_id=" + request.json["profile_id"])

    with open('ui_exports//properties.csv', 'w', newline='', encoding='utf-8') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)


        spamwriter.writerow( [ "id", "landfield_id", "for_sale", "description", "location", "center", "price", "country", "tile_count", "current_value", "trading_value", "tile_class", "tile_class_revenue", "update_time" ] )
        for property in r.json():
            spamwriter.writerow( [ property["id"], property["landfield_id"], property["for_sale"], property["description"], property["location"], property["center"], property["price"], property["country"], property["tile_count"], property["current_value"], property["trading_value"], property["tile_class"], property["tile_class_revenue"], property["update_time"]  ] )


    return render_template('properties_export.html')   


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
                TILE_CLASS_REVENUE=property_payload["tileClassRevenue"],
                UPDATE_TIME=cur_time,
                PROFILE_ID=profile_id )
            
            final_property_json_str.append(prop)
        
        final_property_json = '[' + ','.join(final_property_json_str) + ']'
        print(final_property_json)
  
        r = requests.post(BACKEND_API+"properties/db", json=json.loads(final_property_json) )
        status_codes.append(r.status_code)
        

        

    return render_template('properties_load.html',status_codes=status_codes)