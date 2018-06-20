"""
Reads a file of keys words and returns the percent match of keywords to a int
"""
import pandas as pd

#original_working_dir = os.getcwd()
#print(' ')
#print('original_working_dir     = ' + str(original_working_dir))


#find the key words of interest
keyword = pd.read_csv("../data/input_keywords.csv")
keywords = list(keyword["keywords"])

lc_keywords = []
for k in keywords:
    lc_keywords.append(k.lower())

def percent_match(input_description):
    #input: description, a string
    #output: percent of keywords found, for example 66.67
    description = input_description.lower()
    counter = 0
    for k in lc_keywords:
        if k in description:
            counter += 1
    foo = round(((counter/(len(lc_keywords)))* 100), 2)
    return (foo)
    #percent_match.append(f"{foo}%")
    
#def test_percent_match():
#    print(percent_match('python'))