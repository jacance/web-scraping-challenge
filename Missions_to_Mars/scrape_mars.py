#!/usr/bin/env python
# coding: utf-8


from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import time
import pymongo

import requests

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

db = client.mars_db

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    browser = init_browser() 
    mars_dict = {}   

    # First website to scrape for news title and paragraph
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    mars_dict["news_title"] = soup.find('div',class_='content_title').text
    mars_dict["news_p"] = soup.find('div',class_='rollover_description_inner').text



    # Second website to scrape for image
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    browser.visit(url)

    time.sleep(1)
    browser.click_link_by_partial_text("FULL IMAGE")
    browser.click_link_by_partial_text("more info")

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    results = soup.find_all('figure', class_="lede")
    for result in results:
        image_url = result.a['href']
        mars_dict["featured_image_url"] = f"https://www.jpl.nasa.gov{image_url}"
    


    
    # Third website to scrape for image url and title of the 4 hemispheres
    mars_url = "https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced"

    # List containing the names of the 4 hemispheres
    mars_hemispheres = ['cerberus', 'schiaparelli', 'syrtis_major', 'valles_marineris']

    # Parse target url
    response = requests.get(mars_url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Add hemisphere name and image url to dictionary
    for hemisphere in mars_hemispheres:
        mars_url = f'https://astrogeology.usgs.gov/search/map/Mars/Viking/{hemisphere}_enhanced'
        response = requests.get(mars_url)
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.find_all("img", class_='wide-image')
        
        for result in results:
            img_url = result.get('src')
            title = soup.find("h2", class_='title').text
            title = title.replace(' Enhanced',"")
            mars_dict[f'{hemisphere}_title'] = title
            mars_dict[f'{hemisphere}_img_url'] = 'https://astrogeology.usgs.gov' + img_url

            
    db.mars_info.insert_one(mars_dict)

    browser.quit()  

    return mars_dict
    
    # collection name
    