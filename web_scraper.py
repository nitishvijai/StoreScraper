import requests
from bs4 import BeautifulSoup

print('Gathering eBay listings...')
URL = 'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313.TR12.TRC2.A0.H0.Xsamsung+galaxy+note+9.TRS0&_nkw=samsung+galaxy+note+9&_sacat=0&LH_TitleDesc=0&_osacat=0&_odkw=samsung+galaxy+s9+plus'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')
ebay_results = soup.find(id='mainContent')

ebay_listings = ebay_results.find_all('li', class_='s-item')

runs = 0
for listing in ebay_listings:
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

print('Gathering Sears listings...')

URL_s = 'https://www.sears.com/search=samsung%20galaxy%20note%209'
page_s = requests.get(URL_s)

soup_s = BeautifulSoup(page_s.content, 'html.parser')

sears_results = soup_s.find(id='cards-holder')

sears_listings = sears_results.find_all('div', class_='card-container card-border')

runs = 0
for listing in sears_listings:
    if runs >= 1: break
    itemTag = soup_s.find('h3', class_='card-title')
    item_element = itemTag.a['title']
    item_price = listing.find('span', class_='card-price ng-binding ng-scope card-price-orig')
    if None in (item_element, item_price):
        continue
    print(item_element)
    print(item_price.text.strip())
    print()
    print()
    runs += 1    

sears_price = item_price.text.strip()

print ('Gathering Sam\'s Club listings...')

URL_sc = 'https://www.samsclub.com/s/samsung%20galaxy%20note%209'
page_sc = requests.get(URL_sc)

soup_sc = BeautifulSoup(page_sc.content, 'html.parser')

sams_results = soup_sc.find('div', class_='sc-infinite-loader sc-product-cards analytics')

sams_listings = sams_results.find_all('div', class_="sc-product-card sc-product-card-grid sc-product-card-has-flag")

runs = 0
for listing in sams_listings:
    if runs >= 1: break
    item_element = listing.find('div', class_="sc-product-card-title")
    itemTag = listing.find('span', class_="Price-group")
    if None in (item_element, itemTag, item_price):
       continue
    print(item_element.text.strip())
    print(itemTag.attrs.get('title').replace('current price: ', ''))
    print()
    print()
    runs += 1

sams_price = item_price.text.strip()

print('Comparing the three prices...')

elected_link = ''
elected_price = 0.00

if (sears_price >= sams_price) and (sears_price >= ebay_price):
    elected_link = URL_s
    elected_price = sears_price
elif (sams_price >= sears_price) and (sams_price >= ebay_price):
    elected_link = URL_sc
    elected_price = sams_price
else:
    elected_link = URL
    elected_price = ebay_price

print('Here\'s the link to the lowest price. Have fun!')
print(elected_link)
print(elected_price)