
# Import splinter and BeautifulSoup

from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

# also impord pandas that will help us scrape an entire table
import pandas as pd


# lets now set the paths for our executables

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

def mars_news(browser):
    # visit the mars nasa news site

    url = 'http://redplanetscience.com/'
    browser.visit(url)

    #optional delay for loading the page

    browser.is_element_present_by_css('div.list_text', wait_time=1)


    # now lets set up the HTML parser

    html = browser.html
    news_soup = soup(html, 'html.parser')
    slide_elem = news_soup.select_one('div.list_text')

    # Add try/except for error handling
    try:
        # let's start scraping

        slide_elem.find('div', class_='content_title')


        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        


        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None
    
    return news_title, news_p


# ### Featured Images

def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)


    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()



    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')


    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        img_url_rel

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url

### MARS FACTS

def mars_facts():
    
    # Add try/except for error handling
   
    try:
        
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    
    # Assign columns and set index of dataframe
    
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()


