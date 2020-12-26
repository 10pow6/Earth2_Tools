import csv
import time
import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


# Disable image load to prevent E2 server's from crying more (use less bandwidth)
option = webdriver.ChromeOptions()
chrome_prefs = {}
option.experimental_options["prefs"] = chrome_prefs
chrome_prefs["profile.default_content_settings"] = {"images": 2}
chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}

# Setup our driver with options and open designated URL
driver = webdriver.Chrome(chrome_options=option)  # Optional argument, if not specified will search path.
driver.get( "https://earth2.io" )


current_page = 99
tiles = driver.find_elements_by_class_name("card")

for tile in tiles:
                data = tile.text.splitlines()
                tile_url = tile.find_element_by_tag_name("a").get_attribute("href")
                tile_size = data[0].split()[0]
                tile_alias = data[1]
                tile_market_rate = data[3]
                tile_purchase_rate = data[5]
                # fix to account for buy properties additional data
                if( len( data) > 9 ):
                    tile_gps = data[10].split(" ")
                    tile_location = data[11]
                else:
                    tile_gps = data[7].split(" ")
                    tile_location = data[8]
                # some lat long combos do not play nicely and caused this split to crash
                # explore why at some later point
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