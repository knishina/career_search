# Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import requests
import platform

def scrape(search_zip_code,search_job_title):
    print(search_zip_code, search_job_title)
    glassdoor_url="https://www.glassdoor.com/index.htm"

    operating_system = platform.platform()
    
    if operating_system[0:4] == "Wind":
        executable_path = {'executable_path': 'chromedriver.exe'}
        browser1 = Browser('chrome', **executable_path, headless=True)
    else:
        executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
        browser1 = Browser("chrome", **executable_path, headless=True)

    #when calling glassdoor, populate the job title and zipcode followed by submit buttion
    
    browser1.visit(glassdoor_url)
    browser1.fill('sc.keyword',search_job_title)
    browser1.find_by_css('.loc').fill(str(search_zip_code))
    browser1.find_by_css('.gd-btn-mkt').first.click()

    #get the source code of the browser
    html1 = browser1.html

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html1, 'html.parser')

    # Examine the results, then determine element that contains sought info
    # print(soup.prettify())

    glass_door_data={}
    title=[]
    company=[]
    city=[]
    state=[]
    url=[]
    description=[]
    
    #for the rows returned populate the list of title, company, city, url, state
    
    results = soup.find_all("li", class_="jl")
    for i in range(len(results)):
        link = results[i].find('div', class_="flexbox").find('a', class_="jobLink")["href"]
        title_text = results[i].find('div', class_="flexbox").find('a', class_="jobLink").text 

        title.append(title_text)
        url.append(f'https://www.glassdoor.com{link}')

        company.append(results[i].find('div', class_="flexbox empLoc").find('div').text.split(' – ')[0].lstrip())

        a,b = results[i].find("span", class_="subtle loc").text.split(",")
        city.append(a)
        state.append(b[1:3])  

    if operating_system[0:4] == "Wind":
        executable_path = {'executable_path': 'chromedriver.exe'}
        browser3 = Browser('chrome', **executable_path, headless=True)
    else:
        executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
        browser3 = Browser("chrome", **executable_path, headless=True)

    #for each listing get the description using url
        
    for link in url:
        job_desc_url = link 
        browser3.visit(job_desc_url)
        html3 = browser3.html
        soup3 = BeautifulSoup(html3, 'html.parser')

        try:
            job_desc = soup3.find("div",class_="jobDescriptionContent desc module pad noMargBot collapsed noPadBot")
            description.append(job_desc.text)
        except:
            print(job_desc_url)
            job_desc = soup3.find("body")
            description.append(f"'{job_desc}'")


    print(f"Glassdoor Len of URL {len(url)}")
    print(f"Glassdoor Len of company {len(company)}")
    print(f"Glassdoor Len of title {len(title)}")
    print(f"Glassdoor Len of state {len(state)}")
    print(f"Glassdoor Len of city {len(city)}")
    print(f"Glassdoor Len of description {len(description)}")

    #return the data as list of dictionaries
    
    glassdoor_db = []
    for i in range(len(url)):
            glassdoor_dict = {}
            glassdoor_dict["title"] = title[i]
            glassdoor_dict["company"] = company[i]
            glassdoor_dict["city"] = city[i]
            glassdoor_dict["state"] = state[i]
            glassdoor_dict["url"] = url[i]
            glassdoor_dict["description"] = description[i]
            glassdoor_db.append(glassdoor_dict)

    return glassdoor_db

from splinter import Browser
def init_browser():
    executable_path = {"executable_path", "/user/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless = False)
