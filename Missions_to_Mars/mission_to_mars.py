#!/usr/bin/env python
# coding: utf-8


# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import requests

import pandas as pd

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_websites = {}


# # NASA Mars News


url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'


response = requests.get(url)
response




soup = BeautifulSoup(response.text, 'html.parser')




print(soup.prettify())




results = soup.find_all("div", class_="slide")
results




for result in results:
    news_title = result.find("a").text
    news_p = result.find("div", class_="rollover_description_inner").text
    


# # JPL Mars Space Images - Featured Image



executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)



browser.click_link_by_partial_text('FULL IMAGE')
browser.click_link_by_partial_text("more info")




html = browser.html
soup = BeautifulSoup(html, 'html.parser')
results = soup.find_all("figure", class_="lede")

for result in results:
    image_url = result.a['href']
    featured_image_url = f'https://www.jpl.nasa.gov{image_url}'




featured_image_url




browser.quit()


# # Mars Facts



import pandas as pd




url = 'https://space-facts.com/mars/'




tables = pd.read_html(url)
len(tables)



mars_df = tables[0]
mars_df = mars_df.rename(columns={0:"",1:"Mars"}).set_index("")
mars_df




mars_df.to_html('mars_html.html')


# # Mars Hemispheres



mars_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'

mars_hemispheres = ['cerberus', 'schiaparelli', 'syrtis_major', 'valles_marineris']




response = requests.get(mars_url)
soup = BeautifulSoup(response.text, "html.parser")




hemisphere_image_urls = []

for hemisphere in mars_hemispheres:
    mars_url = f'https://astrogeology.usgs.gov/search/map/Mars/Viking/{hemisphere}_enhanced'
    response = requests.get(mars_url)
    soup = BeautifulSoup(response.text, "html.parser")
    results = soup.find_all("img", class_='wide-image')
    
    for result in results:
        img_url = result.get('src')
        title = soup.find("h2", class_='title').text
        title = title.replace(' Enhanced',"")
        mars_dict = {
            "title": title,
            "img_url": 'https://astrogeology.usgs.gov' + img_url
        }
        hemisphere_image_urls.append(mars_dict)
    




hemisphere_image_urls



mars_df = pd.DataFrame(hemisphere_image_urls)
mars_df






