from urlparse import* 
import bs4 as bs
import urllib.request
import json
import time
import pandas as pd

basket = []
columns = [      
                "name",
                "link",
                "image",
                
                "price",
                "discount",
                "discountprice",
                "harddiscount",
                "harddiscountprice",

                "merchantName",
                "brandName",
                "productId",
                "categoryId",
                "categoryName"]


url = input("url")
url = "https://www.hepsiburada.com/yorganlar-c-510009?sayfa=3"

def getHepsiburadaSinglePage( url , page = 1 ):

    goToUrl = paginateUrl(url, page)
    sauce = urllib.request.urlopen(goToUrl)
    getsauce = sauce.read()
    soup = bs.BeautifulSoup(getsauce, "lxml")

    items = []
    for item in soup.find_all('li', attrs = {'class' : 'search-item'} ):

        row = {}
        for col in columns:
            row[col] = ""

            
        #get defaults
        row['name'] = item.h3.span.text
        row['image'] = item.img.get('src')
        row['link'] = item.a.get('href')
        button = item.button

   

        #prices
        price_container = item.find('', attrs = {'class' : 'price-container'} )

        if item.find('del', attrs = {'class' : 'product-old-price'} ) is not None:
            row['price']    = item.find('del', attrs = {'class' : 'product-old-price'} ).text
            row['discount'] = item.find('div', attrs = {'class' : 'discount-badge'} ).span.text
        
        row['discountprice'] = item.find('span', attrs = {'class' : 'price'} ).text

        hasharddiscount = item.find('div', attrs = {'class' : 'last-price'} )
        
        if  hasharddiscount is not None:
            row['harddiscountprice'] = item.find('div', attrs = {'class' : 'price-value'} ).text
            row['harddiscount'] = item.find('div', attrs = {'class' : 'green-text'} ).span.text

 
        if  button is not None:
            meta = button.get('data-product')
            jsonmeta = json.loads(meta)

            row["merchantName"] = jsonmeta['merchantName']
            row["brandName"] = jsonmeta['brandName']
            row["productId"] = jsonmeta['productId']
            row["categoryId"] = jsonmeta['categoryId']
            row["categoryName"] = jsonmeta['categoryName']
            
            #print(jsonmeta)
            #print(type(jsonmeta))
 
       return row

getHepsiburadaSinglePage(url)
