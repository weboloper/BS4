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


#url = input("url")
#url = "https://www.hepsiburada.com/yorganlar-c-510009?sayfa=3"

def getSinglePageResults( url , page = 1 ):

    goToUrl = paginateUrl(url, page)
    print("Requesting : " + goToUrl)
    sauce = urllib.request.urlopen(goToUrl)
    getsauce = sauce.read()
    soup = bs.BeautifulSoup(getsauce, "lxml")

    results = []
    for item in soup.find_all('li', attrs = {'class' : 'search-item'} ):

        row = {}
        for col in columns:
            row[col] = ""

            
        #get defaults
        row['name'] = item.h3.span.text
        row['image'] = item.img.get('src')
        row['link'] = "https://www.hepsiburada.com/" + item.a.get('href')
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


        results.append(row)

    print("Page " + str(page) + " successfuly scrapped" )
    return results


#getSinglePageResults(url)


def getTotalPages(url):

    goToUrl = paginateUrl(url, 1)
    sauce = urllib.request.urlopen(goToUrl)
    getsauce = sauce.read()
    soup = bs.BeautifulSoup(getsauce, "lxml")

    pagination = soup.find("div", {"id": "pagination"})
    lastpage = pagination.find_all("li")[-1].text

    return lastpage.strip()

def scrapHepsiburada(url, limit = 1):

    if(limit < 1 ) :
        limit = int(getTotalPages(url))

    print(str(limit) + " total pages will be scrapped")

    results = []
    for page in range(1, limit + 1):

        print("Checking Page " + str(page) + "...")
        time.sleep(1)
        result = getSinglePageResults(url, page )

        results = results + result
        if(limit > 1 ):
            time.sleep(5)

    print( str(len(results)) + " search results scrapped")

    return results
    #writeExcel(results)

#scrapHepsiburada(url, 2)


