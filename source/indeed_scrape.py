# Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import requests
import platform

def scrape(search_zip_code,search_job_title):

    #meta_input = "../data/input_meta.csv"
    #df=pd.read_csv(meta_input,low_memory=False)
    #search_zip_code = df["zip"][0]
    #search_job_title = df["job_title"][0]

    indeed_url=f"https://www.indeed.com/jobs?as_and={search_job_title}&as_phr=&as_any=&as_not=&as_ttl=&as_cmp=&jt=all&st=&salary=&radius=50&l={search_zip_code}&fromage=3&limit=5&sort=&psf=advsrch"
    
    operating_system = platform.platform()
    
    if operating_system[0:4] == "Wind":
        executable_path = {'executable_path': 'chromedriver.exe'}
        browser1 = Browser('chrome', **executable_path, headless=True)
    else:
        executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
        browser1 = Browser("chrome", **executable_path, headless=True)

    # URL of page to be scraped
    indeed_search_results = indeed_url 
    browser1.visit(indeed_search_results)

    try:
        browser1.click_link_by_id(id="prime-popover-close-button")
    except:
        print("no popup")

        
    #get the source code of the browser
    html1 = browser1.html

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html1, 'html.parser')

    # Examine the results, then determine element that contains sought info
    # print(soup.prettify())

    title=[]
    company=[]
    city=[]
    state=[]
    url=[]
    description=[]

    #for the rows returned populate the list of title, company, city, url, state
    
    results = soup.find_all("div", class_="row result clickcard")
    for i in range(len(results)):
        title.append(results[i].find('a', class_="turnstileLink").text)
        url.append(f'https://www.indeed.com{results[i].a["href"]}')

        company_name = results[i].find("span", class_="company").text.split("\n")

        for row in company_name:
            if row != " ":
                name = row

        company.append(name.lstrip())
        try:
            a,b = results[i].find("span", class_="location").text.split(",")
            city.append(a)
            state.append(b[1:3])
        except:
            city.append("San Jose")
            state.append("CA")
    
    print("=============Result 1===============")
    print(f"Indeed Len of URL {len(url)}")
    print(f"Indeed Len of company {len(company)}")
    print(f"Indeed Len of title {len(title)}")
    print(f"Indeed Len of state {len(state)}")
    print(f"Indeed Len of city {len(city)}")
    print(f"Indeed Len of description {len(description)}")            
            
    results = soup.find_all("div", class_="lastRow row result clickcard")
    for i in range(len(results)):
        title.append(results[i].find('a', class_="turnstileLink").text)
        url.append(f'https://www.indeed.com{results[i].a["href"]}')

        company_name = results[i].find("span", class_="company").text.split("\n")

        for row in company_name:
            if row != " ":
                name = row

        company.append(name.lstrip())
        
        try:
            a,b = results[i].find("span", class_="location").text.split(",")
            city.append(a)
            state.append(b[1:3])
        except:
            city.append("San Jose")
            state.append("CA")
            
    print("=============Result 2===============")
    print(f"Indeed Len of URL {len(url)}")
    print(f"Indeed Len of company {len(company)}")
    print(f"Indeed Len of title {len(title)}")
    print(f"Indeed Len of state {len(state)}")
    print(f"Indeed Len of city {len(city)}")
    print(f"Indeed Len of description {len(description)}")                        
    results = soup.find_all("div", class_="row sjlast result clickcard")
    
    for i in range(len(results)):
        title.append(results[i].find('a', class_="turnstileLink").text)
        url.append(f'https://www.indeed.com{results[i].a["href"]}')

        company_name = results[i].find("span", class_="company").text.split("\n")

        for row in company_name:
            if row != " ":
                name = row
        
        company.append(name.lstrip())
        
        try:
            a,b = results[i].find("span", class_="location").text.split(",")
            city.append(a)
            state.append(b[1:3])
        except:
            city.append("San Jose")
            state.append("CA")
            
    print("=============Result 3===============")
    print(f"Indeed Len of URL {len(url)}")
    print(f"Indeed Len of company {len(company)}")
    print(f"Indeed Len of title {len(title)}")
    print(f"Indeed Len of state {len(state)}")
    print(f"Indeed Len of city {len(city)}")
    print(f"Indeed Len of description {len(description)}")                    

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
            job_desc = soup3.find("span",id="job_summary")
            description.append(job_desc.text)
        except:
            print(job_desc_url)
            job_desc = soup3.find("body")
            description.append(f"'{job_desc}'")

    indeed_db = []

    #return the data as list of dictionaries
    
    for i in range(len(url)):
        indeed_dict = {}
        indeed_dict["title"] = title[i]
        indeed_dict["company"] = company[i]
        indeed_dict["city"] = city[i]
        indeed_dict["state"] = state[i]
        indeed_dict["url"] = url[i]
        indeed_dict["description"] = description[i]
        indeed_db.append(indeed_dict)
    
    return indeed_db

from splinter import Browser
def init_browser():
    executable_path = {"executable_path", "/user/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless = False)
