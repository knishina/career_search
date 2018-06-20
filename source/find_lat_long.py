"""
Functions to get the latitude and longitdue given a company name and city.


"""

import pandas as pd
import requests
import json
from google_api_key import *
from google_lat_long_api_key import *

#Get the google api key, stored two levels (directories) up. 
#Then return to the orginal working directory
#The intent is it won't get accidentaly PUSHed got gitHub
if 0:
    import os
    print('***Tring to get the google geoCoding lat long API key***')
    original_working_dir = os.getcwd()
    print('original_working_dir     = ' + str(original_working_dir))
    os.chdir('..\..') #go up two levels to get the google api key
    print('looking for google_api_key.py in  = ' + str(os.getcwd()))
    from google_lat_long_api_key import *
    print('changing back to original working directory. ' + str(original_working_dir))
    os.chdir(original_working_dir)
    print('current working direcory = ' + str(os.getcwd()))

def build_google_lat_long_query_sting(point_of_interest):
    base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    query_str = base_url + 'address='+ point_of_interest +   '&key=' + api_lat_long_key
    return query_str
#https://maps.googleapis.com/maps/api/geocode/json?address=intel+santa clara&key=
    
def get_lat_long(point_of_interest):
    query_str = build_google_lat_long_query_sting(point_of_interest)
    r = requests.get(query_str)
    data = r.json()
    try:
        lat = data['results'][0]["geometry"]["location"]['lat']
        long = data['results'][0]["geometry"]["location"]['lng']  
    except:
        print(data)
        print(point_of_interest)
        lat = 0
        long = 0        
    return {'lat':lat,'long':long}

def test_lat_long():
    life = get_lat_long('intel santa clara')
    print(str(life))
  
