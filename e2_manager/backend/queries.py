
import requests
import json
from string import Template


class E2Queries:
    # set as instance variables to support initialization with different files in the future
    def __init__( self ):
        self.DEBUG=False
        self.E2_ENDPOINT="https://app.earth2.io/graphql"

        self.ERROR_DEBUG_MODE = '{ "errors": [{ "status": "-1", "detail": "DEBUG MODE ENABLED."}]}'
        self.ERROR_NO_COUNTRY = '{ "errors": [{ "status": "-1", "detail": "No countries input for query."}]}'
        self.ERROR_INVALID_COUNTRY = '{ "errors": [{ "status": -1, "detail": "Invalid country in query"}]}'

        self.E2_COUNTRIES = ["NU","US","__"]

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
