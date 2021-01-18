
import requests
import json
from string import Template


class E2Queries:
    # set as instance variables to support initialization with different files in the future
    def __init__( self ):
        self.DEBUG=False
        self.E2_ENDPOINT="https://app.earth2.io/graphql"

        self.ERROR_INVALID_PROFILE = '{ "errors": [{ "status": -1, "detail": "Invalid profile id in query"}]}'
        self.ERROR_DEBUG_MODE = '{ "errors": [{ "status": "-1", "detail": "DEBUG MODE ENABLED."}]}'
        self.ERROR_NO_COUNTRY = '{ "errors": [{ "status": "-1", "detail": "No countries input for query."}]}'
        self.ERROR_INVALID_COUNTRY = '{ "errors": [{ "status": -1, "detail": "Invalid country in query"}]}'

        self.E2_COUNTRIES = ["__","AD","AE","AF","AG","AI","AL","AM","AO","AQ","AR","AS","AT","AU","AW","AX","AZ","BA","BB","BD","BE","BF","BG","BH","BI","BJ","BL","BM","BN","BO","BQ","BR","BS","BT","BV","BW","BY","BZ","CA","CC","CD","CF","CG","CH","CI","CK","CL","CM","CN","CO","CR","CU","CV","CW","CX","CY","CZ","DE","DJ","DK","DM","DO","DZ","EC","EE","EG","EH","ER","ES","ET","FI","FJ","FK","FM","FO","FR","GA","GB","GD","GE","GF","GG","GH","GI","GL","GM","GN","GP","GQ","GR","GS","GT","GU","GW","GY","HK","HM","HN","HR","HT","HU","ID","IE","IL","IM","IN","IO","IQ","IR","IS","IT","JE","JM","JO","JP","KE","KG","KH","KI","KM","KN","KP","KR","KW","KY","KZ","LA","LB","LC","LI","LK","LR","LS","LT","LU","LV","LY","MA","MC","MD","ME","MF","MG","MH","MK","ML","MM","MN","MO","MP","MQ","MR","MS","MT","MU","MV","MW","MX","MY","MZ","NA","NC","NE","NF","NG","NI","NL","NO","NP","NR","NU","NZ","OM","PA","PE","PF","PG","PH","PK","PL","PM","PN","PR","PS","PT","PW","PY","QA","RE","RO","RS","RU","RW","SA","SB","SC","SD","SE","SG","SH","SI","SJ","SK","SL","SM","SN","SO","SR","SS","ST","SV","SX","SY","SZ","TC","TD","TF","TG","TH","TJ","TK","TL","TM","TN","TO","TR","TT","TV","TW","TZ","UA","UG","UM","US","UY","UZ","VA","VC","VE","VG","VI","VN","VU","WF","WS","YE","YT","ZA","ZM","ZW","xy"]

        self.graphql_get_countries = """
        { 
            getTilePrices(countries: [ $TARGET ]) {countryCode, tradeAverage, final, totalTilesSold } 
        }
        """

        self.graphql_get_transactions = """
        {
            getBalanceChanges(items: $ITEM_COUNT, page: $PAGE, balanceChangeTypeFilter: "$FILTER_TYPE") {
                count
                balanceChanges {
                    description
                    balanceChangeTypeDisplay
                    createdDisplay
                    amount
                    countryFlag
                    balanceBefore
                    balanceAfter
                    landfield {
                        id
                        description
                        tileCount
                        location
                    }
                }
            }
        }
        """

        self.graphql_get_properties = """
        query {
            getUserLandfields(
                userId: "$PROFILE_ID"
                page: $PAGE
                items: $PROPERTY_COUNT
            ) {
                count
                landfields {
                    id
                    forSale
                    description
                    location
                    center
                    price
                    country
                    tileCount
                    currentValue
                    tradingValue
                    tileClass
                }
            }
        }
        """

        self.graphql_get_properties_count = """
        query {
            getUserLandfields(
                userId: "$PROFILE_ID"
                page: 1
                items: 1
            ) {
                count
            }
        }
        """

    def __run_query(self,query, session_id = None): # A simple function to use requests.post to make the API call. Note the json= section.
        cookies = {}
        if session_id is not None:
            cookies = {'sessionid': session_id }

        request = ''
        if( self.DEBUG ):
            print("E2_ENDPOINT: ", self.E2_ENDPOINT )
            print("GRAPHQL Query: ", query )
            print("COOKIES: ", cookies)
 
            return json.loads(self.ERROR_DEBUG_MODE)
        else:
            request = requests.post(self.E2_ENDPOINT, json={'query': query}, cookies=cookies)

        if request.status_code == 200:
            response = request.json()
            return response
        else:
            return '{ "errors": [{ "status": "-1", "detail": "' + format(request.status_code, query) + '"}]}'



    ##################################################
    # Country Processing
    ##################################################   
    def __valid_country(self, country):
        return country in self.E2_COUNTRIES

    def __build_graphql_get_countries( self, countries ):
        if( len(countries) < 1 ):
            return False,json.loads(self.ERROR_NO_COUNTRY)
        replacement_string = ''
        for country in countries:
            if( self.__valid_country( country ) ):
                replacement_string += '"' + country + '"' + ","
            else:
                return False,json.loads(self.ERROR_INVALID_COUNTRY)

        replacement_string = replacement_string[:-1]

        return True,Template(self.graphql_get_countries).substitute(TARGET=replacement_string)
    
    def get_countries_data(self, countries ):
        query = self.__build_graphql_get_countries(countries )

        if( query[0] ):
            return self.__run_query(query[1] )
        else:
            return query



    ##################################################
    # Property Processing
    ##################################################   
    def __build_graphql_get_properties_count( self, profile_id ):
        if( len(profile_id) != 36 ):
            return False,json.loads(self.ERROR_INVALID_PROFILE)
        return True,Template(self.graphql_get_properties_count).substitute(PROFILE_ID=profile_id)
    
    def get_properties_count(self, profile_id ):
        query = self.__build_graphql_get_properties_count(profile_id )

        if( query[0] ):
            return self.__run_query(query[1] )
        else:
            return query

    def __build_graphql_get_properties( self, profile_id, page, property_count ):
        if( len(profile_id) != 36 ):
            return False,json.loads(self.ERROR_INVALID_PROFILE)
        return True,Template(self.graphql_get_properties).substitute(PROFILE_ID=profile_id,PAGE=page,PROPERTY_COUNT=property_count)
    
    def get_properties(self, profile_id, page, property_count ):
        query = self.__build_graphql_get_properties(profile_id, page, property_count )

        if( query[0] ):
            return self.__run_query(query[1] )
        else:
            return query