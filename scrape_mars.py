#import dependencies
import bs4
from bs4 import BeautifulSoup
import requests
import splinter
from splinter import Browser
import pandas as pd

def scrape():
    #set up connection
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)

    #visit nasa news site
    nasa_url = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_url)
    html = browser.html
    nasasoup = BeautifulSoup(html,'html.parser')

    #find most recent news title and description
    result = nasasoup.find_all(class_="slide")
    news_title = result[0].find('h3').text
    news_p = result[0].find(class_='rollover_description_inner').text

    #visit jpl.nasa site
    nasa_url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(nasa_url2)
    html = browser.html
    nasasoup2 = BeautifulSoup(html, 'html.parser')

    #get imageurl for featured image
    featuredimageurl = 'https://www.jpl.nasa.gov' + nasasoup2.select('#full_image')[0]['data-fancybox-href']

    #visit twitter
    twitterfeed_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitterfeed_url)
    html = browser.html
    twittersoup = BeautifulSoup(html,'html.parser')

    #get most recent weather tweet
    mars_weather = twittersoup.find('p',class_="TweetTextSize").text

    #visit space-facts.com
    spacefacts_url = 'https://space-facts.com/mars/'
    browser.visit(spacefacts_url)
    html = browser.html
    spacefactsoup = BeautifulSoup(html,'html.parser')

    #read in table via pandas
    spacefacttabledf = pd.read_html(html)[0]

    #convert table back to html
    spacefacttable = spacefacttabledf.to_html(index=False)

    #visit usgs.gov
    usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(usgs_url)

    #grab hemisphere name and img_url for each of the four hemispheres
    imagelinks = []
    for x in range(4):
        links = browser.find_link_by_partial_text('Enhanced')
        browser.click_link_by_partial_text(links[x].text)
        html = browser.html
        imagesoup = BeautifulSoup(html,'html.parser')
        result = imagesoup.find('a',text='Sample')
        hemistring = imagesoup.find('h2').text
        imagelinks.append({'title':hemistring[:len(hemistring)-9],'img_url':result.attrs['href']})
        browser.back()

    output = {'news_title':news_title, 'news_p':news_p, 'featuredimageurl':featuredimageurl,
              'mars_weather':mars_weather,'spacefacttable':spacefacttable, 'imagelinks':imagelinks}

    return output
