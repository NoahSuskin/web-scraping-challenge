import pandas as pd
from bs4 import BeautifulSoup as bs
import time
from splinter import Browser
import html5lib


def open_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)


# In[4]:
def scrape():

    browser = open_browser()

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    time.sleep(5)

    html = browser.html
    soup = bs(html, 'html.parser')
    browser.is_element_present_by_css("ul.item_list li.slide")

    # In[5]:

    items_list = soup.find_all('div', class_='list_text')
    item = soup.find('div', class_='list_text')
    title = item.find('div', class_='content_title').text

    # In[7]:

    date = item.find('div', class_='list_date').text
    title_p = item.find('div', class_='article_teaser_body').text

    # In[8]:

    # JPL Mars Images - Scrapping Featured Image

    # In[9]:

    # In[10]:

    # JPL Mars Images - Scrapping Featured Image
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)

    time.sleep(5)

    image_html = browser.html
    image_soup = bs(image_html, 'lxml')

    # In[11]:

    # print(image_soup.prettify)

    # In[12]:

    browser.links.find_by_partial_text('FULL IMAGE')
    browser.links.find_by_partial_text('more info')
    # image_urls = image_soup.find_all('div', class_='carousel_items')
    image_list_t = image_soup.find_all('article')
    image_list = image_soup.find('article')
    image_url_v = image_list.find('a')
    image_url = image_url_v['data-fancybox-href']

    # In[13]:

    featured_image_url = f'https://www.jpl.nasa.gov{image_url}'

    # In[14]:

    # Mars Weather

    # In[15]:

    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)

    time.sleep(5)

    twitter_html = browser.html
    twitter_soup = bs(twitter_html, 'lxml')

    # In[16]:

    weather_list_items = twitter_soup.find_all('div',
                                               class_='css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0')[
        0]
    mars_weather = weather_list_items.find('span',
                                           class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0').text

    # In[17]:

    # Mars Facts

    # In[18]:

    mars_facts_url = 'https://space-facts.com/mars/'

    # In[19]:

    mars_facts_df = pd.read_html(mars_facts_url)[0]
    mars_facts_df.columns = ['Measurement', 'Value']
    mars_facts_df.set_index('Measurement', inplace=True)
    mars_facts = mars_facts_df.to_html()
    # In[20]:

    # Mars Hemisphere

    # In[21]:

    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)

    time.sleep(5)

    hemisphere_html = browser.html
    hemisphere_soup = bs(hemisphere_html, 'lxml')

    # In[22]:

    hemi_image_urls = []
    hemi_list = hemisphere_soup.find_all('div', class_='item')
    for item in hemi_list:
        url = 'https://astrogeology.usgs.gov/'

        title = item.find('h3').text
        title = title.replace('Enhanced', '')
        link = item.find('a')['href']
        full_link = url + link

        executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
        browser = Browser('chrome', **executable_path, headless=False)
        browser.visit(full_link)
        html = browser.html
        soup = bs(html, 'lxml')

        time.sleep(5)

        downloads = soup.find('div', class_='downloads')
        image = downloads.find('a')['href']

        entry = {'title': title, 'image': image}
        hemi_image_urls.append(entry)

    final_data = {'title': title, 'title_p': title_p, 'featured_image_url': featured_image_url,
                  'mars_weather': mars_weather, 'mars_facts': mars_facts, 'hemi_image_urls': hemi_image_urls}

    browser.quit()

    return final_data


if __name__ == '__main__':
    scrape()




    







