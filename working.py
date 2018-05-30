import bs4 as bs
import urllib.request
import json
import time
import pandas as pd



def getHepsiBuradaMostSales(category_name , page_number):

    sauce = urllib.request.urlopen("https://www.hepsiburada.com/" + str(category_name) + "?siralama=coksatan&sayfa="+ str(page_number))
    getsauce = sauce.read()
    soup = bs.BeautifulSoup(getsauce, "lxml")

    
    productNames = []
    productLinks = []
    productImages = []

    productPrice = []
    productDiscount = []
    productOldPrice = []
    
    productExtraDiscount = []
    productExtraOldPrice = []

    productIds = []
    productMerchants = []
    productBrands = []
    productCategoriesIds = []
    productCategories =[]
    
    for item in soup.find_all('li', attrs = {'class' : 'search-item'} ):

        #get defaults
        title = item.h3.span.text
        image = item.img.get('src')
        link = item.a.get('href')
        button = item.button

        #prices
        price_container = item.find('', attrs = {'class' : 'price-container'} )
        oldprice = 0
        discount = 0
        price = 0
        extraprice = 0
        extradiscount = 0

        if item.find('del', attrs = {'class' : 'product-old-price'} ) is not None:
            oldprice = item.find('del', attrs = {'class' : 'product-old-price'} ).text
            discount = item.find('div', attrs = {'class' : 'discount-badge'} ).span.text
        
        price = item.find('span', attrs = {'class' : 'price'} ).text

        hasextradiscount = item.find('div', attrs = {'class' : 'last-price'} )
        
        if  hasextradiscount is not None:
            extraprice = item.find('div', attrs = {'class' : 'price-value'} ).text
            extradiscount = item.find('div', attrs = {'class' : 'green-text'} ).span.text

        #prices
        #price = item.find('span', attrs = {'class' : 'product-price'} ).text
        #oldprice = 0
        #discount = 0
        #if item.find('del', attrs = {'class' : 'product-old-price'} ) is not None:
        #oldprice = item.find('del', attrs = {'class' : 'product-old-price'} ).text
        #discount = item.find('div', attrs = {'class' : 'discount-badge'} ).span.text

        #check meta        
        #meta = button.get('data-product')
        #jsonmeta = json.loads(meta)

  
        if  button is not None:
            meta = button.get('data-product')
            jsonmeta = json.loads(meta)
            print(jsonmeta)
             
        productNames.append(title)
        productLinks.append(link)
        productImages.append(image)

        

        #row =  [ title  ]
        #print( row )
    #test_df = pd.DataFrame({'name': productNames , 'link' : productLinks , 'image' : productImages     })
    #print(test_df.info())
        


#getHepsiBuradaMostSales("mutfak-ekipmanlari-c-237529" , 3)

def getHepsiBuradaMostSalesPageCount(category_name):
    sauce = urllib.request.urlopen("https://www.hepsiburada.com/" + str(category_name) + "?siralama=coksatan")
    getsauce = sauce.read()
    soup = bs.BeautifulSoup(getsauce, "lxml")

    pagination = soup.find("div", { "id" : "pagination" })

    lastpage = pagination.find_all("li")[-1].get_text()
    
    return lastpage

#getHepsiBuradaMostSalesPageCount("mutfak-ekipmanlari-c-237529")

for page_number in range(1,  int(getHepsiBuradaMostSalesPageCount("beyaz-esya-mutfak-urunleri-c-2147483637"))):   
    getHepsiBuradaMostSales("beyaz-esya-mutfak-urunleri-c-2147483637" , page_number )
    time.sleep(5)
