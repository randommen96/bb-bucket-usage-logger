# import python modules
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from csv import DictWriter
import requests
import time
import re
from datetime import date
from datetime import datetime
from os import getenv
from dotenv import load_dotenv
from pyotp import *
import telegram_send

# define selenium driver
chrome_options = Options()
chrome_options.add_argument("--user-data-dir=selenium_b2use")
chrome_options.add_argument("--headless")
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1920,1080')

driver = webdriver.Chrome(options=chrome_options)

# define variables
load_dotenv()
usernamebb=getenv('USERNAMEBB')
passwordbb=getenv('PASSBB')
totp=TOTP(getenv('TOTP'))
repattern="(\d+,)?(\d+)?.\d+ (GB|MB)"
bucketsizes=[]
today = date.today()
now = datetime.now()
current_time = now.strftime("%H:%M:%S")

def bb_login():
    driver.get ("https://secure.backblaze.com/user_signin.htm")

def bb_login_username():
    driver.find_element_by_class_name("email-field").send_keys(usernamebb)
    driver.find_element_by_css_selector("button.bz-btn.bz-btn-blue.bz-btn-lg").click()

def bb_login_password():
    driver.find_element_by_class_name("password-field").send_keys(passwordbb)
    driver.find_element_by_css_selector("button.bz-btn.bz-btn-blue.bz-btn-lg").click()
    
def bb_login_otp(): 
    #OTP check
    try:
        if driver.find_element_by_css_selector("h3.sign-in-form-title").text == "Two-Factor Verification":
            token = totp.now()
            driver.find_element_by_class_name("code-field").send_keys(token)
            cb_otp = driver.find_element_by_class_name("bz-switch-circle").click()
            time.sleep(1)
            driver.find_element_by_css_selector("button.bz-btn.bz-btn-blue.bz-btn-lg").click()
        else:
            print("Al ingelogd")
    except:
        pass

def bb_getdata():
    global statsdata
    global bucketnames
    statsdata = driver.find_elements_by_css_selector("div.b2-stats-data")
    bucketnames = driver.find_elements_by_css_selector("div.b2-bucket-bucket-name")

def bb_parsedata():
    global bucketsizes
    for stda in statsdata:
        x = re.search(repattern, stda.text)
        if x:
            bucketsizes.append(x.group(0))
        else:
            pass          

def bb_returndata():
    totalsize = 0
    telegram_messagedata = ""
    for bucket, bucketsize in zip(bucketnames, bucketsizes):
        telegram_messagedata += bucket.text + " is " + bucketsize + " groot.\n"
        if bucketsize[-3:] == " GB":
            size = float(bucketsize[:-3].replace(',', ''))
            totalsize += size
        elif bucketsize[-3:] == " MB":
            size = bucketsize[:-3].replace(',', '')
            size = float(size) / 1000
            totalsize += size
        field_names = ['bucketname','bucketsize','date','time']
        row_dict = {'bucketname': bucket.text,'bucketsize': bucketsize,'date': today,'time': current_time}
        # Append a dict as a row in csv file
        append_dict_as_row('bucketlog.csv', row_dict, field_names)
    telegram_messagedata += "totale ruimte in gebruik is " + str(round(totalsize, 2)) + " GB."
    print(telegram_messagedata)
    telegram_send.send(messages=[telegram_messagedata], conf="telegram-send.conf")

def append_dict_as_row(file_name, dict_of_elem, field_names):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        dict_writer = DictWriter(write_obj, fieldnames=field_names)
        # Add dictionary as wor in the csv
        dict_writer.writerow(dict_of_elem)


def bb_logout():
    driver.get ("https://secure.backblaze.com/user_logout.htm")

def bb_quit():
    driver.quit()

# login procedure
bb_login()
time.sleep(5)
bb_login_username()
time.sleep(5)
bb_login_password()
time.sleep(5)
bb_login_otp()
time.sleep(5)

# get data from bb
bb_getdata()
time.sleep(2)

# make data usable
bb_parsedata()

# return data
bb_returndata()

# end session gracefully
bb_logout()
time.sleep(1)
bb_quit()