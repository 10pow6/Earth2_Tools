##############################################
#  
# If you like this, please use referral code
#     1PKLXGV109
#
# For 5% off game tiles!
#
##############################################
#
# Release: v1
# Description: Goes through your property pages and extracts relevant information to CSV (excel dialect)
#
###############################################

import csv
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


############# UPDATE THIS STRING ##########################
# The URL to your profile page which lists all properties
############# UPDATE THIS STRING ##########################
E2_PROFILE_URL="Put your profile URL here"

# Timeout for initial page load
TIMEOUT=35
# Override for crashes.  0 for no change
START_PAGE = 0 
# Override for crashes.  0 for no change
END_PAGE = 0


# Disable image load to prevent E2 server's from crying more (use less bandwidth)
option = webdriver.ChromeOptions()
chrome_prefs = {}
option.experimental_options["prefs"] = chrome_prefs
chrome_prefs["profile.default_content_settings"] = {"images": 2}
chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}

# Setup our driver with options and open designated URL
driver = webdriver.Chrome(chrome_options=option)  # Optional argument, if not specified will search path.
driver.get( E2_PROFILE_URL )


try:
    # We wait until the pagination list has loaded (the class pagination is always present, so we need to see the list items)
    element_present = EC.presence_of_element_located((By.CSS_SELECTOR , "li.active"))
    WebDriverWait(driver, TIMEOUT).until(element_present)

    print("~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Page Anchor Element Found")
    print("~~~~~~~~~~~~~~~~~~~~~~~~")

    # capture max pages
    pagination = driver.find_element_by_class_name("pagination")
    items = pagination.find_elements_by_tag_name("li")

    # strip your navigation left and right
    items = items[1:-1]
    
    min_page = items[0].text
    max_page = items[-1].text

    print("~~~ MIN PAGE = ", min_page)
    print("~~~ MAX PAGE = ", max_page)
    print("~~~~~~~~~~~~~~~~~~~~~~~~")

    counter = 0

    with open("prop_export.csv", "w", newline="", encoding="utf-8") as csvfile:
        propwriter = csv.writer(csvfile, dialect="excel")

        # note: we lack error handling because this was just thrown together :)

        # manage start page override
        if( START_PAGE != 0 ):
            # navigate to where we want
            driver.find_element_by_link_text(items[START_PAGE - 1].text).click()
            print( "Skipping to page ", START_PAGE )

            # prep for for loop
            START_PAGE -= 1
            counter = START_PAGE

            # This can be automated based on content changes.  Lazy atm though ;)
            input("Press Enter After Next Page Loads...")

        # manage end page override
        if( END_PAGE == 0 ):
            END_PAGE = int(max_page)

        row = [ "Page", "Prop_URL", "Prop_Size", "Prop_Alias", "Prop_MarketRate", "Prop_PurchaseRate", "Prop_Lon", "Prop_Lat", "Prop_Location"]
        propwriter.writerow( row )


        for i in range(START_PAGE,END_PAGE):
            # capture all tiles information on page
            tiles = driver.find_elements_by_class_name("card")
            
            active_li =  pagination.find_element_by_css_selector("li.active")
            current_page = active_li.text

            for tile in tiles:
                data = tile.text.splitlines()

                tile_url = tile.find_element_by_tag_name("a").get_attribute("href")
                tile_size = data[0].split()[0]
                tile_alias = data[1]
                tile_market_rate = data[3]
                tile_purchase_rate = data[5]
                tile_gps = data[7].split(" ")

                # fix to account for buy properties additional data
                if( len( data) > 9 ):
                    tile_gps = data[10].split(" ")
                    try:
                        tile_location = data[11]
                    except:
                        tile_location = "NaN"
                else:
                    tile_gps = data[7].split(" ")
                    try:
                        tile_location = data[8]
                    except:
                        tile_location = "NaN"

                # some lat long combos do not play nicely and caused this split to crash
                # I think this was related to the buy properties.  Don't want to remove
                # this piece as it works as is... but probably unecessary now.
                tile_lon = tile_gps[0]
                tile_lat = ""
                if( len(tile_gps) > 1 ):
                    tile_lat = tile_gps[1]
                
                print("Current Page: ", current_page)
                print("Tile URL: ", tile_url )
                print("Tile Size: ", tile_size)
                print("Tile Alias: ", tile_alias)
                print("Tile Market Rate: ", tile_market_rate)
                print("Tile Purchase Rate: ", tile_purchase_rate)

                # lat/lon are reverse in E2
                print("Tile GPS Lon: ", tile_lon)
                print("Tile GPS Lat: ", tile_lat)
                               

                print("Tile Location: ", tile_location)
                print("===============================")


                row = [ current_page, tile_url, tile_size, tile_alias, tile_market_rate, tile_purchase_rate, tile_lon, tile_lat, tile_location]
                propwriter.writerow( row )

            counter += 1
            if( counter < len(items) ):
                driver.find_element_by_link_text(items[counter].text).click()

                print( "= Clicked Page Link ", items[counter].text, " ")
                
                # This can be automated based on content changes.  Lazy atm though ;)
                input("Press Enter After Next Page Loads...")
    
except TimeoutException:
    print("Timed out waiting for page to load")

input("All done, Enter to continue (small delay before closing)...")
time.sleep(5) # Let the user actually see something!

driver.quit()