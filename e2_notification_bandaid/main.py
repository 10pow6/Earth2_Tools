import httpx
from string import Template
import sys
sys.stdout.reconfigure(encoding='utf-8')


API="https://app.earth2.io/graphql"

uid = "YOUR USER ID HERE"
pg = 1
itm = 1

QUERY_properties_template = """
query {
    getUserLandfields(
        userId: "$USER_ID"
        page: $PAGE
        items: $ITEMS
    ) {
        count
        landfields {
            id
            description
            bidentrySet
            {
              created
              offerSet
              {
                created
                modified
                user
                {
                  username
                }
                value
              }

            }
        }
    }
}

"""


data = Template(QUERY_properties_template).substitute(USER_ID=uid, PAGE=pg, ITEMS=itm)


response = httpx.post( API, json={'query': data})
data = response.json()

itm = 60

counts = int(data["data"]["getUserLandfields"]["count"])
pages = int( counts/itm) + (counts % itm > 0)



for i in range(1,pages+1):
    print("<br><br>=======================")
    print("Page: " + str(pg))
    print("=======================")
    data = Template(QUERY_properties_template).substitute(USER_ID=uid, PAGE=pg, ITEMS=itm)
    response = httpx.post( API, json={'query': data})
    data = response.json()
    for landfield in data["data"]["getUserLandfields"]["landfields"]:
        if len( landfield["bidentrySet"] ) > 0:
            link = "https://app.earth2.io/#thegrid/" + landfield["id"]
            description = ( landfield["description"] + "  |  ")
            html = '<br><a href="' + link + '" target="new">' + description + link + "</a>"
            print( html )
    pg = pg + 1