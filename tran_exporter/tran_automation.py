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
# Description: Goes through your transaction pages and extracts relevant information to CSV (excel dialect)
#
###############################################

import csv
import time
import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


# FYI
E2_PROFILE_URL="https://app.earth2.io/#transactions"

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
driver.get( "https://earth2.io" )
input("Please login and navigate to start page of transactions then press enter.  Make sure browser is not in mobile format.")


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

    with open("tran_export.csv", "w", newline="", encoding="utf-8") as csvfile:
        propwriter = csv.writer(csvfile, dialect="excel")

        # note: we lack error handling because this was just thrown together :)

        # manage start page override
        if( START_PAGE is not 0 ):
            # navigate to where we want
            driver.find_element_by_link_text(items[START_PAGE - 1].text).click()
            print( "Skipping to page ", START_PAGE )

            # prep for for loop
            START_PAGE -= 1
            counter = START_PAGE

            # This can be automated based on content changes.  Lazy atm though ;)
            input("Press Enter After Next Page Loads...")

        # manage end page override
        if( END_PAGE is 0 ):
            END_PAGE = int(max_page)

        row = [ "Page", "Country Flag", "Property Location", "Property Size", "Transaction Type", "Transaction Date", "Transaction Amount", "Balance"]
        propwriter.writerow( row )


        for i in range(START_PAGE,END_PAGE):
            # capture all tiles information on page
            transactions = driver.find_elements_by_class_name("row")
            # strip out header 
            transactions = transactions[1:]
            
            active_li =  pagination.find_element_by_css_selector("li.active")
            current_page = active_li.text

            for tran in transactions:
                data = tran.text.splitlines()

                tran_flag = tran.find_element_by_tag_name("img").get_attribute("src")

                if len(data) > 2:
                    tran_loc = data[0]
                    tran_prop_size = data[1]
                    tran_type = re.search(r'[a-zA-Z\s\(\)]+', data[2]).group(0)
                    tran_date = re.search(r'\d{4}-\d{2}-\d{2}', data[2]).group(0)
                    bals = re.search(r'[-+]\$[^\]]+', data[2]).group(0)
                else: #fix for null locations
                    tran_loc = "NULL LOCATION"
                    tran_prop_size = data[0]
                    tran_type = re.search(r'[a-zA-Z\s\(\)]+', data[1]).group(0)
                    tran_date = re.search(r'\d{4}-\d{2}-\d{2}', data[1]).group(0)
                    bals = re.search(r'[-+]\$[^\]]+', data[1]).group(0)

                bals = bals.split()
                tran_amt = bals[0]
                tran_bal = bals[1]

                print("Transaction Flag: ", tran_flag)
                print("Transaction Location: ", tran_loc)
                print("Transaction Prop Size: ", tran_prop_size)
                print("Transaction Type: ", tran_type)
                print("Transaction Date: ", tran_date)
                print("Transaction Amt: ", tran_amt)
                print("Balance: ", tran_bal)

                row = [ current_page, tran_flag, tran_loc, tran_prop_size, tran_type, tran_date, tran_amt, tran_bal ]
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