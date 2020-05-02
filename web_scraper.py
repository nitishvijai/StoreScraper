# libraries

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from requests_html import HTMLSession

# global variables

headers = {
    'Host': 'www.amazon.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'TE': 'Trailers'
}

binary = FirefoxBinary('C:\\Program Files\\Mozilla Firefox\\firefox.exe')
options = webdriver.FirefoxOptions()
options.add_argument('-headless')
driver = webdriver.Firefox(firefox_binary=binary, executable_path=r'C:\\BrowserDriver\geckodriver.exe', firefox_options=options)

# main code

search = input('Enter the item you want to search for: ')
print()
print('Searching for ' + search)

# eBay

search = search.replace(' ', '+')

print('Gathering eBay listings...')
URL_e = 'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313.TR12.TRC2.A0.H0.Xnitish.TRS0&_nkw=' + search
page = requests.get(URL_e)

soup = BeautifulSoup(page.content, 'html.parser')
results = soup.find(id='mainContent')

listings = results.find_all('li', class_='s-item')

runs = 0
for listing in listings:
    if runs >= 1: break
    item_element = listing.find('h3', class_='s-item__title')
    item_price = listing.find('span', class_='s-item__price')
    if None in (item_element, item_price):
        continue
    print(item_element.text.strip())
    print(item_price.text.strip())
    print()
    print()
    runs += 1

ebay_price = item_price.text.strip()
ebay_price = ebay_price.replace('$','')
ebay_price = float(ebay_price)

session = HTMLSession()

# Amazon

print('Gathering Amazon listings...')

URL = 'https://www.amazon.com/s?k=' + search

driver.get(URL)
page = requests.get(URL, headers=headers)

soup = BeautifulSoup(driver.page_source, 'html.parser')

runs = 0
results = soup.findAll('span', attrs={'class': 'a-size-base-plus a-color-base a-text-normal'})
for listing in results:
    if runs >= 1: break
    print(soup.select_one('span.a-size-base-plus').get_text())
    runs += 1

runs = 0
results = soup.findAll('span', attrs={'class': 'a-offscreen'})
for listing in results:
    if runs >= 1: break
    element = soup.select_one('span.a-offscreen')
    if None in element:
        continue
    print(element.get_text())
    print()
    print()
    runs += 1

amazon_price = element.get_text()
amazon_price = amazon_price.replace('$','')
amazon_price = float(amazon_price)

# Best Buy

print ('Gathering Best Buy listings...')

URL_bb = 'https://www.bestbuy.com/site/searchpage.jsp?st=' + search

driver.get(URL_bb)
page = requests.get(URL_bb, headers=headers)

soup = BeautifulSoup(driver.page_source, 'html.parser')

runs = 0
results = soup.findAll('h4', attrs={'class': 'sku-header'})
for listing in results:
    if runs >= 1: break
    print(soup.select_one('h4.sku-header').get_text())
    runs += 1

runs = 0
results = soup.findAll('div', attrs={'class': 'priceView-hero-price priceView-customer-price'})
for listing in results:
    if runs >= 1: break
    element = soup.select_one('div.priceView-customer-price > span:first-child')
    if None in element:
        continue
    print(element.get_text())
    print()
    print()
    runs += 1

bb_price = element.get_text()
bb_price = bb_price.replace('$','')
bb_price = float(bb_price)

# Final price comparison

print('Comparing the three prices...')

elected_link = ''
elected_price = 0.00

if (ebay_price <= amazon_price) and (ebay_price <= bb_price):
    elected_price = ebay_price
    elected_link = URL_e
elif (amazon_price <= ebay_price) and (amazon_price <= bb_price):
    elected_price = amazon_price
    elected_link = URL
elif (bb_price <= ebay_price) and (bb_price <= amazon_price):
    elected_price = bb_price
    elected_link = URL_bb

print('Here\'s the link to the lowest price. Have fun!')
print(elected_link)
print('$' + str(elected_price))

# Execution halts here