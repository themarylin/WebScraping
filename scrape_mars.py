from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from splinter import Browser
import time
import tweepy
import selenium
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


def scrape():
    final_data = {}
    output = marsNews()
    final_data['mars_news'] = output[0]
    final_data['mars_paragraph'] = output[1]
    final_data['mars_image'] = marsImage()
    final_data['mars_weather'] = marsWeather()
    final_data['mars_facts'] = marsFacts
    final_data['mars_hemisphere'] = marsHem()
    return final_data


def marsNews():
    url = 'https://mars.nasa.gov/news'
    # Retrieve page with the requests module
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    output = []
    output.append(soup.find('div', class_="content_title").text.strip())
    output.append(soup.find('div', class_="rollover_description").text.strip())
    return output


def marsImage():
    html = browser.html
    soup = bs(html, 'html.parser')
    feature_title = soup.find('h1', class_='media_feature_title').text
    feature_title = feature_title.strip()
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    time.sleep(1)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(1)

    jpl_html = browser.html
    jpl_soup = bs(jpl_html, 'html.parser')

    img_relative = jpl_soup.find('img', class_='fancybox-image')['src']
    image_path = f'https://www.jpl.nasa.gov{img_relative}'
    return image_path


def marsWeather():
    from keys import consumer_key, consumer_secret, access_token, access_token_secret
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
    target_user = "marswxreport"
    full_tweet = api.user_timeline(target_user , count = 1)
    mars_weather=full_tweet[0]['text']
    return mars_weather


def marsFacts():
    url = 'http://space-facts.com/mars/'
    tables = pd.read_html(url)
    df = tables[0]
    html_table = df.to_html()
    return html_table


def marsHem():
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html = browser.html
    soup = bs(html, "html.parser")
    mars_hemisphere = []

    products = soup.find("div", class_ = "result-list" )
    hemispheres = products.find_all("div", class_="item")
    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup=bs(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        mars_hemisphere.append({"title": title, "img_url": image_url})
    return mars_hemisphere
