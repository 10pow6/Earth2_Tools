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

# capture all tiles information on page
transactions = driver.find_elements_by_class_name("row")
# strip out header 
transactions = transactions[1:]

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
