"""
Reads the combined database and returns the top ten matches that are in the specified driving time.
"""
# import dependencies
import pandas as pd
import pymongo
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# link to the appropriate database
db = client.career_search
entries = db.combined_db.find()

# define the last scrape and the commute time provided by user
last_pull_time = db.combined_db.distinct("timestamp")[-1]
commute_input_time = db.combined_db.distinct("input_commute_time_in_mins")[-1]

# run the query and append it to a list
query = db.combined_db.find({"timestamp":last_pull_time, "commute_dur_sec": {'$lte':commute_input_time}})
listy = []
for q in query:
    listy.append(q)

# take the list, put into a df and sort on percent_match in descending order
# return only the first 10 rows
df = pd.DataFrame(listy)
result = df.sort_values("percent_match", ascending=False)[0:10]
