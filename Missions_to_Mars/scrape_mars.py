# with a function called scrape that will execute all of your 
#scraping code and 
# return one Python dictionary containing all of the scraped data.

# Import dependencies 
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import Browser
from flask import Flask, render_template, redirect
from webdriver_manager.chrome import ChromeDriverManager

# initialize the browser for the scrape
def init_browser():
    executable_path = {'executeable_path': 'chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    # initialize dictionary for scraped data
    mars_dict = {}

    # scrape latest news from nasa mars
    nasa_mars_url = "https://mars.nasa.gov/news"
    browser.visit(nasa_mars_url)
    html = browser.html
    soup = bs(html,'html.parser')

    # grab latest news title
    news_title = soup.find_all('div', class_='content_title')[1].text

    # grab corresponding paragraph
    news_p = soup.find_all('div', class_='article_teaser_body')[0].text
    
    # jpl featured image scrape
    jpl_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(jpl_url)
    html = browser.html
    soup = bs(html,'html.parser')
    featured_image = soup.find('div',class_='floating_text_area').a['href']
    featured_image_url = jpl_url + featured_image

    # mars facts scrape
    mars_facts_url = "https://space-facts.com/mars/"
    browser.visit(mars_facts_url)
    mars_table = pd.read_html(mars_facts_url)
    mars_facts = pd.DataFrame(mars_table)
    mars_facts_html = mars_facts.to_html()
    mars_facts_html.replace('\n','')

    # mars hemisphere image scrape
    mars_hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(mars_hemisphere_url)
    html = browser.html
    soup = bs(html,'html.parser')
    mars_hemispheres = soup.find('div',class_='collapsible results')
    mars_item = mars_hemispheres.find_all('div',class_='item')
    hemisphere_image_urls = []

    # loop through each item to get title and image url
    for item in mars_item:
        # error handling
        try:
            # grab title in h3 text of div class "description"
            hemisphere = item.find('div', class_='description')
            title = hemisphere.h3.text
        
            # grab image url in <a href a\>
            # go to hemisphere url
            hemisphere_url = hemisphere.a['href']
            browser.visit('https://astrogeology.usgs.gov' + hemisphere_url)
            html = browser.html
            soup = bs(html,'html.parser')
            image_url = soup.find('li').a['href']
        
            if (title and image_url):
                # print results
                print('-------------------------------------')
                print(title)
                print(image_url)
            
            # create dictionary for title and url
            hemisphere_dict={
                'title': title,
                'image_url': image_url
            }
            hemisphere_image_urls.append(hemisphere_dict)
        except Exception as e:
            print(e)
        
        # create dictionary for scraped data above
        mars_dict = {
            "news_title": news_title,
            "news_p": news_p,
            "featured_image_url":featured_image_url,
            "mars_facts_html":mars_facts_html,
            "hemisphere_images": hemisphere_image_urls
        }

        # close browser
        browser.quit()
        return mars_dict


