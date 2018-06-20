from flask import Flask, render_template, jsonify, redirect, session, request
import pymongo
import json
from flask_pymongo import PyMongo, pymongo
import indeed_scrape
import glassdoor_scrape
import random
import datetime
import pandas as pd
import travel_time
import percent_match
import find_lat_long

app = Flask(__name__)

client = pymongo.MongoClient()
db = client.career_search

app.secret_key = 'secretkey'

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/scrape", methods=['POST'])
def scrape():
    
    start_locn = request.form['start_locn']
    city = request.form['city']
    state = request.form['state']
    zipcode = request.form['zip']
    job_title = request.form['job_title']
    commute_start_time = request.form['commute_start_time']
    commute_time_in_mins1 = request.form['commute_time_in_mins']
    commute_time_in_mins = int(commute_time_in_mins1) * 60   # actually cheating by converting it to seconds and not changing the label.
    
    print(start_locn,city,zipcode,state,job_title,commute_start_time, commute_time_in_mins)
    
    if 'id' not in session: #this is a new session
        session['id']=random.random()
    else:
        print(session['id']) #this id has already been set for this 
        
    timestamp =  str(datetime.datetime.now())
    
    #Call the glassdorr and indeed scrape function to extract raw data and store to the DB
    #when storing include additional fields as mentioned below
    
    indeed_data = indeed_scrape.scrape(zipcode,job_title)
    glassdoor_data = glassdoor_scrape.scrape(zipcode,job_title)
    
    for row in glassdoor_data:
        row["timestamp"]=timestamp
        row["session_id"]=session['id']
        row["data_source"]="Glassdoor"
        row["input_start_locn"] = start_locn
        row["input_city"] = city
        row["input_state"] = state
        row["input_zipcode"] = zipcode
        row["input_job_title"] = job_title
        row["input_commute_start_time"] = commute_start_time
        row["input_commute_time_in_mins"] = commute_time_in_mins

    for row in indeed_data:
        row["timestamp"]=timestamp
        row["session_id"]=session['id']
        row["data_source"]="Indeed"
        row["input_start_locn"] = start_locn
        row["input_city"] = city
        row["input_state"] = state
        row["input_zipcode"] = zipcode
        row["input_job_title"] = job_title
        row["input_commute_start_time"] = commute_start_time
        row["input_commute_time_in_mins"] = commute_time_in_mins

    db.indeed_db.insert(indeed_data)
    db.glassdoor_db.insert(glassdoor_data)
    
    #Remove duplicates using pandas
    #1. convert list of dictionaries in pandas dataframe and merge them
    #2. convert to upper case on fields to be marked as dup
    #3. remove duplicates on city comany title and state and keep the last row from duplicate

    df1 = pd.DataFrame.from_dict(indeed_data)
    
    df1["city"]=df1["city"].str.upper()
    df1["state"]=df1["state"].str.upper()
    df1["company"]=df1["company"].str.upper()
    df1["title"]=df1["title"].str.upper()

    df2 = pd.DataFrame.from_dict(glassdoor_data)
    
    df2["city"]=df2["city"].str.upper()
    df2["state"]=df2["state"].str.upper()
    df2["company"]=df2["company"].str.upper()
    df2["title"]=df2["title"].str.upper()
    
    combined_db_dataframe = pd.concat([df1,df2])
    combined_db_dataframe.drop_duplicates(subset=['city', 'company', 'title'], keep="last",inplace=True)
    
    #convert dataframes to list of dictornies and insert in database
    
    combined_db = combined_db_dataframe.to_dict('records')
    
    #using the combined_db which has no duplicates, get the latittude, long, percent match and other infor by calling the 
    #appropriate functions
    
    for row in combined_db:
        
        point_of_interest = f'{row["company"]} {row["city"]} {row["state"]}'
        start_address = f'{start_locn} {zipcode}'
        
        travel_time_dict = travel_time.get_travel_one_way_travel_time(start_address,point_of_interest,commute_start_time)
        travel_time_over_the_day = travel_time.get_travel_time_over_the_day(start_address,point_of_interest)
        
        cordinates = find_lat_long.get_lat_long(point_of_interest)
        
        row["latitude"] = cordinates["lat"]
        row["longitude"] = cordinates["long"]
        row["x_axis_time_of_day"] = travel_time_over_the_day["x_axis_time_of_day"]
        row["y_axis_travel_time_sec"] = travel_time_over_the_day["y_axis_travel_time_sec"]
        row["commute_time_of_day"] = travel_time_dict["commute_time_of_day"]
        row["commute_dur_sec"] = travel_time_dict["commute_dur_sec"]
        row["communte_dur_text"] = travel_time_dict["communte_dur_text"]
        row["percent_match"] = percent_match.percent_match(row["description"])
    
    #store the combined data in to the database

    db.combined_db.insert(combined_db)
    return render_template("results.html")

@app.route("/data")
def data():
    entries = db.combined_db.find()

    # define the last scrape and the commute time provided by user
    last_pull_time = db.combined_db.distinct("timestamp")[-1]
    commute_input_time = db.combined_db.distinct("input_commute_time_in_mins")[-1]

    # run the query and append it to a list
    # take the list, put into a df and sort on percent_match in descending order
    # return only the first 10 rows
    query = db.combined_db.find({"timestamp":last_pull_time, "commute_dur_sec": {'$lte':commute_input_time}}).sort("percent_match", pymongo.DESCENDING).limit(10)
    listy = []
    for q in query:
        listy.append(q)
    df = pd.DataFrame(listy)

    y_travel_time_int = []
    for y in df["y_axis_travel_time_sec"]:
        new_list = []
        for x in y:
            foobar =  int(x.replace(" mins", ""))
            new_list.append(foobar)
        y_travel_time_int.append(new_list)
    df["y_axis_travel_time_sec"] = y_travel_time_int

    x_time_of_day = []
    for x in df["x_axis_time_of_day"]:
        new_listy = []
        for thing in x:
            foo = int(thing.replace(":0", ""))
            new_listy.append(foo)
        x_time_of_day.append(new_listy)
    df["x_axis_time_of_day"] = x_time_of_day

    df1 = df[["city", "communte_dur_text", "commute_dur_sec", "company", "data_source", "latitude", "longitude", "percent_match", "input_city", "title", "url", "x_axis_time_of_day", "y_axis_travel_time_sec"]]
    df_json = df1.to_json(orient="records")
    return df_json


@app.route("/results")
def results():
    
    
    return render_template("results.html")

if __name__ == "__main__":
    app.run(debug = True)
    
