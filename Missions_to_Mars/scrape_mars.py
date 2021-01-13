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
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    results = soup.find_all('ul',class_='item_list')

    for result in results:
        mars_dict["news_title"] = result.find('div',class_='content_title').text
        mars_dict["news_p"] = result.find('div',class_='article_teaser_body').text

    browser.quit()

    # Second website to scrape for featured image
    # Navigate to main page of JPL Nasa
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Use xpath of navbar to navigate to Featured Image
    time.sleep(1)
    xpath = '/html/body/div/div/div/header/div[1]/div[3]/div/nav/div[1]/div[4]/button/span'
    browser.find_by_xpath(xpath).click()

    time.sleep(1)
    xpath = '/html/body/div/div/div/header/div[1]/div[3]/div/nav/div[1]/div[4]/div/div/div/div/div[1]/div/div/div/a/p[1]'
    browser.find_by_xpath(xpath).click()

    time.sleep(1)
    xpath = '/html/body/div/div/div/main/div/div[2]/div/div/div[2]/button/span'
    browser.find_by_xpath(xpath).click()

    # Extract featured image using BeautifulSoup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find_all('div', class_='BaseLightbox__slide__img')

    for result in results:
        featured_image_url = result.img['src']
        mars_dict["featured_image_url"] = featured_image_url

    browser.quit()


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
    
    