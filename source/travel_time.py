"""
Functions to get the travel time between two locations given a time of day.
Example calls are in test_drive_time()

Function get_travel_time_over_the_day() will return a dataFrame of travel times for the entire day.

"""

import pandas as pd
import requests
import json
import time
import calendar
import requests
import numpy as np
import matplotlib.pyplot as plt
from google_api_key import *
from google_lat_long_api_key import *

#Get the google api key, stored two levels (directories) up. 
#Then return to the orginal working directory
#The intent is it won't get accidentaly PUSHed got gitHub

if 0:
    import os
    print('***Tring to get the google API key***')
    original_working_dir = os.getcwd()
    print('original_working_dir     = ' + str(original_working_dir))
    os.chdir('..\..') #go up two levels to get the google api key
    print('looking for google_api_key.py in  = ' + str(os.getcwd()))
    from google_api_key import *
    print('changing back to original working directory. ' + str(original_working_dir))
    os.chdir(original_working_dir)
    print('current working direcory = ' + str(os.getcwd()))

def convert_str_for_query(input_str):
    #prep a str for a query to google.  
    #     Replace ' ', with '+'
    #     Replace ',', with '+'
    output_str = input_str.replace(' ','+')
    output_str = output_str.replace(',','+')
    output_str = output_str.replace('+++','+')
    output_str = output_str.replace('++','+')
    
    return output_str

def convert_time_of_day_to_epoch(time_of_day):
    #convert time of day, like '7:30 AM' to epoch time
    time_of_day = time_of_day.replace(' ',':')
    time_of_day_split = time_of_day.split(":")
    if len(time_of_day_split) > 2:
        if 'AM' == time_of_day_split[2].upper():
            hour = int(time_of_day_split[0])   
        elif 'PM' == time_of_day_split[2].upper():
            hour = int(time_of_day_split[0]) + 12
        else:
            #print(time_of_day_split[2])
            return -1
    else:  #no AM or PM listed, so assume AM
        hour = int(time_of_day_split[0])   

    minutes= int(time_of_day.split(':')[1])         
    epoch_time = str(int(time.mktime((2018, 8, 14, hour, minutes, 0, 0, 0, -1))))
    return epoch_time

def build_google_query_sting(start_loc,end_loc,commute_time):
    #build the query_sting for google api for travel time between two points at a certain time of day
    #returns the url for the requests call
    #start_loc is a string containing relavent details for the start of the jurney. For example 'intel santa clara ca'
    #go_to_job_time is time of day, for example '7 AM'
    base_url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
    lang_str = '&language=en-EN'  # language for json return
    mode_str = '&mode=driving'    # mode of transportation between point A and B 
    commute_epoch = convert_time_of_day_to_epoch(commute_time)
    
    start_loc_query_str = convert_str_for_query(start_loc)
    end_loc_query_str = convert_str_for_query(end_loc)
    
    query_str = base_url + 'origins='+ start_loc_query_str + '&destinations=' + end_loc_query_str
    query_str = query_str + mode_str + lang_str  
    query_str = query_str + '&departure_time=' + commute_epoch + '&key=' + api_key
    
    return query_str

## below function for testing purpose
def create_travel_time_graph():
    #This function is not finished out, but gives the rough outline to pull travel time
    #and plot it.
    t_range = pd.date_range("00:00", "23:50", freq="10min").time
    travel_time_sec_array = []
    travel_time_str_array = []
    
    for t in t_range:
        query_home = build_google_query_sting('20675 Broadway 95476','2617 newhall 95050',                                              str(t.hour)+':' + str(t.minute) + ' AM')
        r = requests.get(query_home)
        data = r.json()
        travel_time_sec = data['rows'][0]['elements'][0]['duration_in_traffic']['value']
        travel_time_str = data['rows'][0]['elements'][0]['duration_in_traffic']['text']
        
        travel_time_sec_array.append(travel_time_sec)
        travel_time_str_array.append(travel_time_str)
        time.sleep(0.5)
        
    drive_time_df = pd.DataFrame(data=[t_range,travel_time_sec_array,travel_time_str_array])
    drive_time_df = drive_time_df.transpose()
    drive_time_df.columns = ['commute_time_of_day','commute_dur_sec','communte_dur_text']
    drive_time_df.plot(x='commute_time_of_day',y='commute_dur_sec')
    plt.xticks(rotation=90)
    plt.ylabel('Drive time in seconds')
    plt.show()

def get_travel_time_over_the_day(start_loc,end_loc):
    #Get travel time through out the day from midnight to midnight.  Pass back the dataframe
    t_range = pd.date_range("00:00", "23:50", freq="60min").time
    sleep_sec = 0.1
    travel_time_sec_array = []
    travel_time_str_array = []
    travel_time_time_of_day = []
    number_of_data_points = len(t_range)
    cnt = 0
    for t in t_range:
        query_home = build_google_query_sting(start_loc,end_loc,str(t.hour)+':' + str(t.minute) + ' AM')
        r = requests.get(query_home)
        data = r.json()
        
        try:
            travel_time_sec = data['rows'][0]['elements'][0]['duration_in_traffic']['value']
            travel_time_str = data['rows'][0]['elements'][0]['duration_in_traffic']['text']
            travel_time_sec_array.append(travel_time_sec)
            travel_time_str_array.append(travel_time_str)
            travel_time_time_of_day.append(str(t.hour)+':' + str(t.minute))
        except:
            travel_time_sec_array.append(0)
            travel_time_time_of_day.append(str(t.hour)+':' + str(t.minute))
        
        cnt = cnt + 1
        if (cnt%10 == 0)+(cnt==1):    #give a periodic status update
            print('Completed ' + str(cnt) + ' queries. There are ' + str(number_of_data_points-cnt) + ' points to go. Or ' + str((number_of_data_points-cnt)*sleep_sec) + ' seconds to go.')
        time.sleep(sleep_sec)
    if 0:    
        drive_time_df = pd.DataFrame(data=[t_range,travel_time_sec_array,travel_time_str_array])
        drive_time_df = drive_time_df.transpose()
        drive_time_df.columns = ['commute_time_of_day','commute_dur_sec','communte_dur_text']
        drive_time_df.plot(x='commute_time_of_day',y='commute_dur_sec')
    # debugging plot
    if 0:
        plt.xticks(rotation=90)
        plt.ylabel('Drive time in seconds')
        plt.show()
    return({'x_axis_time_of_day':travel_time_time_of_day,'y_axis_travel_time_sec':travel_time_str_array})

def get_travel_one_way_travel_time(start_loc,end_loc,time_of_day):
    #Get travel time  
    query_str = build_google_query_sting(start_loc,end_loc,time_of_day)
    r = requests.get(query_str)
    data = r.json()

    try:
        travel_time_sec = data['rows'][0]['elements'][0]['duration_in_traffic']['value']
        travel_time_str = data['rows'][0]['elements'][0]['duration_in_traffic']['text']
    except:
        print(data)
        print(start_loc,end_loc,time_of_day)
        travel_time_sec = -1
        travel_time_str = "null"
    
    #drive_time_df = pd.DataFrame(data=[time_of_day,travel_time_sec,travel_time_str])
    #drive_time_df = drive_time_df.transpose()
    #drive_time_df.columns = ['commute_time_of_day','commute_dur_sec','communte_dur_text']
    
    drive_time = {}
    drive_time["commute_time_of_day"] = time_of_day
    drive_time["commute_dur_sec"] = travel_time_sec
    drive_time["communte_dur_text"] = travel_time_str
    
    return drive_time

def test_drive_time():
    one_way_drive_time_df = get_travel_one_way_travel_time('2617 newhall 95050', 'intel santa clara', '7:30 AM')
    print(one_way_drive_time_df)
    one_way_drive_time_df = get_travel_one_way_travel_time('2617 newhall 95050', 'intel santa clara', '5:30 PM')
    print(one_way_drive_time_df)    
