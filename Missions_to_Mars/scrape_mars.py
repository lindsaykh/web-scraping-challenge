# The code below has a function called scrape that will execute all the scraping code from the 
# corresponding mission_to_mars jupyter notebook scraping code. It then returns one Python dictionary 
# containing all of the scraped data called mars_dict.

# Import all necessary dependencies 
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import Browser
from flask import Flask, render_template, redirect
from webdriver_manager.chrome import ChromeDriverManager

# initialize the browser for the scrape (installs as needed)
def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    # executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

# define scrape function based on jupyter notebook components
def scrape():
    browser = init_browser()
    
    # initialize dictionary for scraped data
    mars_dict = {}

    ### scrape latest news from nasa mars ###
    # url info
    nasa_mars_url = "https://mars.nasa.gov/news"
    browser.visit(nasa_mars_url)
    html = browser.html
    soup = bs(html,'html.parser')

    # grab latest news title with beautiful soup find_all text within appropriate div class
    news_title = soup.find_all('div', class_='content_title')[1].text

    # grab corresponding paragraph with beautiful soup find_all text within appropriate div class
    news_p = soup.find_all('div', class_='article_teaser_body')[1].text
    
    ### jpl featured image scrape ###
    # url info
    jpl_url = "https://www.jpl.nasa.gov/images"
    browser.visit(jpl_url)
    html = browser.html
    soup = bs(html,'html.parser')

    # grab the featured image by using beautiful soup find_all 'img' and 'src'
    # from a brute force approach, index 2 was found to correspond to the appropriate image.
    featured_image_url = soup.find_all('img')[2]['src']

    ### mars facts scrape ###
    # url info
    mars_facts_url = "https://space-facts.com/mars/"
    browser.visit(mars_facts_url)

    # read table and create data frame with new column ids and reset index
    mars_table = pd.read_html(mars_facts_url)
    mars_facts = mars_table[0]
    mars_facts = mars_facts.rename(columns = {0:"Description", 1: "Value"})
    mars_facts.set_index("Description",inplace=True)

    # Use Pandas to convert the data to a HTML table string.
    mars_facts_html = mars_facts.to_html()
    mars_facts_html.replace('\n','')

    ### mars hemisphere image scrape ###
    # url info
    mars_hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(mars_hemisphere_url)
    html = browser.html
    soup = bs(html,'html.parser')

    # use beautiful soup to grab hemisphere images from the main page (all are in collapsible results)
    mars_hemispheres = soup.find('div',class_='collapsible results')
    mars_item = mars_hemispheres.find_all('div',class_='item')
    
    # initialize array
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
                # print results in terminal when running (similar to jupyter notebook)
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
            # print errors in terminal if they show up
            print(e)
        
        # create dictionary for scraped data above
        mars_dict = {
            "news_title": news_title,
            "news_p": news_p,
            "featured_image":featured_image_url,
            "mars_facts":mars_facts_html,
            "hemisphere_images": hemisphere_image_urls
        }

        # close browser
        browser.quit()
        return mars_dict


