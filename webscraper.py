from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import pandas as pd
import time

url = 'https://www.airbnb.com/'
#/opt/homebrew/bin/chromedriver
browser = webdriver.Chrome() 

browser.get(url)

# link.click()
def open_search():
    
    path = ".f19g2zq0.dir.dir-ltr"
    browser.find_element(By.CSS_SELECTOR,path).click()

def enter_dest(location):
    location_search = browser.find_element(By.CSS_SELECTOR,'#bigsearch-query-location-input')
    print(location_search)
    time.sleep(1)
    location_search.send_keys(location)

def choose_time():
    when = browser.find_element(By.CSS_SELECTOR,'#search-tabpanel > div > div.chdozwg.dir.dir-ltr > div:nth-child(1) > div')
    when.click()
    im_flexible = browser.find_element(By.CSS_SELECTOR,'#tab--tabs--1') 
    im_flexible.click()
    month = browser.find_element(By.CSS_SELECTOR,'#flexible_trip_lengths-one_month')
    month.click()
    search = browser.find_element(By.CSS_SELECTOR, '#search-tabpanel > div > div.c6ezw63.c1geg2ah.dir.dir-ltr > div.c2frgdd.crbzydf.dir.dir-ltr > div.s1i622mb.dir.dir-ltr > button')
    search.click()

def filters():
    #site-content > div.f15dgkuj.dir.dir-ltr > div.p14tze6r.pj16vlp.dir.dir-ltr > div > div > div > div.b1a88q73.dir.dir-ltr > button
    filter_button = browser.find_element(By.CSS_SELECTOR, '#categoryScroller > div > div > div.f14wfpb5.dir.dir-ltr > div > div > button')
    filter_button.click()


def maxa():
    min = browser.find_element(By.CSS_SELECTOR, '#price_filter_min')
    max = browser.find_element(By.CSS_SELECTOR, '#price_filter_max')
    
    set_limit("0",min)
    set_limit("100", max)
    # /html/body/div[16]/section/div/div/div[2]/div/div[2]/div/footer/div/div/div/footer/a
    # show = browser.find_element('xpath', '/html/body/div[16]/section/div/div/div[2]/div/div[2]/div/footer/div/div/div/footer/a')
    show = browser.find_element(By.CSS_SELECTOR, '._1ku51f04')
    show.click()
    # max.send_keys(Keys.RETURN)

def set_limit(price, path):
    path.click()
    path.send_keys(Keys.BACKSPACE)
    path.send_keys(Keys.BACKSPACE)
    path.send_keys(Keys.BACKSPACE)
    path.send_keys(Keys.BACKSPACE)
    path.send_keys(Keys.BACKSPACE)
    path.send_keys(Keys.BACKSPACE)
    path.send_keys(price) 

def start(dest):
    close_ad()
    open_search()
    enter_dest(dest)
    choose_time()
    time.sleep(4)
    filters()
    time.sleep(2)
    maxa()
    time.sleep(2)
    next_page()
    # browser.get(url)

def close_ad():
    path = '.czcfm7x.dir.dir-ltr'
    browser.find_element(By.CSS_SELECTOR,path).click()

def export_to_xl(data, sheet):
    name = 'Sheet_'+ str(sheet)
    
    with pd.ExcelWriter('output.xlsx') as writer:
        data.to_excel(writer, sheet_name=name)

def next_page():
    page_len = get_pages()
    # listings = []
    listings = []
    for i in range(page_len):
        data = getListings() 
        if len(data) > 0:
            for i in data:
                listings.append(i)
            next_button = browser.find_element(By.CSS_SELECTOR, '._1bfat5l')
            next_button.click()
        time.sleep(2)
    print(listings)
    df = pd.DataFrame(listings)
    if len(listings) > 0:
        df.sort_values(by=['price'], inplace=True)

    export_to_xl(df,1 )
    

def get_pages():
    pages = browser.find_elements(By.CSS_SELECTOR, '._833p2h')
    print(len(pages))
    return len(pages)+1

# scrape site
def getListings():
    listing_list = []
    # listings = browser.find_elements(By.CSS_SELECTOR, '#site-content > div.f15dgkuj.dir.dir-ltr > div.aoez2dw.dir.dir-ltr > div:nth-child(2) > div > div > div > div > div > div > div:nth-child(1) > div')
    listings = browser.find_elements(By.CSS_SELECTOR, '.c4mnd7m.dir.dir-ltr')
    # print(len(listings))
    
    for listing in listings:
        # link  = listing.find_element(By.CSS_SELECTOR, '.ln2bl2p.dir.dir-ltr' ).get_attribute('href')
        link  = listing.find_element(By.CSS_SELECTOR, '.bn2bl2p.dir.dir-ltr' ).get_attribute('href')
        # link  = listing.find_element(By.CSS_SELECTOR, '.cy5jw6o.dir.dir-ltr' ).get_attribute('href')
        price = listing.find_element(By.CSS_SELECTOR, '.a8jt5op.dir.dir-ltr' ).text
        p = price.strip().split()
        # print(p[0])
        if len(p) > 0:
            pr = p[0]
            print(int(pr[1:])),
            listing_item = {
                'price': int(pr[1:]),
                'link': link
            }   
            if listing_item['price'] <= 100:
                listing_list.append(listing_item)
        # print(link,price)
    # df = pd.DataFrame(listing_list)
    # if len(listing_list) > 0:
    #     df.sort_values(by=['price'], inplace=True)

    # if not df.empty:
    #     print(df)
    return listing_list


# class Person:
#   def __init__(self, price, link):
#     self.price = price 
#     self.link = link 


# prev
# class =_1ks8cgb
# curr
# class="_tyxjp1"

    # for each listing
        # get price class  #a8jt5op dir dir-ltrt

    # class="c4mnd7m dir dir-ltr"

    # price class
    # a8jt5op dir dir-ltr

    # link
    # class="ln2bl2p dir dir-ltr"
#price_filter_max