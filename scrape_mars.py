# import dependancies
import time
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    # from splinter import Browser
    executable_path = {'executable_path': ChromeDriverManager().install()}

    browser = Browser('chrome', **executable_path, headless = True)

        # Visit the URL for mars news
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    time.sleep(3)
    # pull html into Beautiful Soup parser
    html=browser.html
    soup=bs(html, 'html.parser')

        # results are returned as an iterable list
    news_elements = soup.find_all('div', class_='list_text')

    # results are returned as an iterable list
    news_elements = soup.find_all('div', class_='list_text')
    news_title = news_elements[0].find('div', class_ = 'content_title').text
    news_p = news_elements[0].find('div', class_ = 'article_teaser_body').text


    # JPL Mars Spave Images
    # Visit the URL for futured images
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    # pull html into Beautiful Soup parser
    html=browser.html
    soup=bs(html, 'html.parser')

    # find the url of the fuatured images
    image = soup.find('img', class_ = 'headerimage fade-in')['src']
    featured_imge_url = url + image

    # Mars Facts
    # Visit the Mars Facts webpage
    mars_facts='https://space-facts.com/mars/'
    mars_fact_table=pd.read_html(mars_facts)

    df = mars_fact_table[0]

    # Create Data Frame
    df.columns = ["Description", "Value"]

    # Set index to Description
    df.set_index("Description", inplace=True)

    # Print Data Frame
    df

    # Save html code to folder Assets
    html_table = df.to_html()

    # Strip unwanted newlines to clean up the table
    html_table.replace("\n", '')

    # Save html code
    # df.to_html("mars_facts_data.html")

    # obtain high resolution images for each of Mar's hemispheres
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # pull html into Beautiful Soup parser
    html=browser.html
    soup=bs(html, 'html.parser')

    # create a list for disctionay of url
    img_title_list = []

    # loop thru the list to retrive High resolution image url and title
    high_reso_image = soup.find_all('div', class_ = 'description')

    for image in high_reso_image: 
        #     title of the image
        image_title = image.find('h3').get_text()
        #     find image url
        img_url = image.find('a', class_ = 'itemLink product-item')['href']
        hemis_url = url + img_url
    #     now find the high resolution image from 'hemis_url'
        browser.visit(hemis_url)
        html = browser.html
        soup = bs(html,'html.parser')
    #     get image src
        img_src = soup.find('img', class_='wide-image')['src']
    #     create image link
        highresol_imgurl = url + img_src
        
    #     create disctionary of titles and high resolution url
        hemisphere_image_url = [{
            'title': image_title,
            'image_url': highresol_imgurl
        }]      
    #      append titles and images to the list
        img_title_list += hemisphere_image_url

    # print(img_title_list)
    for high_res_image in img_title_list:
        
        print(high_res_image['image_url'], high_res_image['title']   
        )

    # create disctionary for all the data from above
    # create disctionary for all the data from above
    mars_information = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_imge_url": featured_imge_url,
        "facts_table": html_table,
        "hemispheres": img_title_list
    }

    # import data to MongoDB
    from pymongo import MongoClient

    client = MongoClient()
    client
    client = MongoClient(host="localhost", port=27017)
    db = client.MissionToMars_DB
    collection = db.marsdata

    collection.insert_one(mars_information)
    return mars_information