import httpx
from bs4 import BeautifulSoup
import pandas as pd
import re
import math


#VATAN COMPUTER / phones
allPhoneData = []

brands = ["apple", "general-mobile", "honor", "huawei", "oppo", "realme", "samsung", "tcl", "tecno", "vivo", "xiaomi"]

for brand in brands:
    response = httpx.get("https://www.vatanbilgisayar.com/{}/cep-telefonu-modelleri/?page={}".format(brand, 1))
    soup = BeautifulSoup(response.content, "html.parser")          
    pageCount = math.ceil(int(re.findall(r'\d+', soup.find("p", {"class": "wrapper-detailpage-header__text"}).text)[0])/16) 
    
    
    for pageNumber in range(1, pageCount+1):
        response = httpx.get("https://www.vatanbilgisayar.com/{}/cep-telefonu-modelleri/?page={}".format(brand, pageNumber))
        soup = BeautifulSoup(response.content, "html.parser")        
        allPhone = soup.find("div", {"id": "productsLoad"}).findAll("div", {"class":"product-list product-list--list-page"})   
        for phone in allPhone:
            
            allPhoneData.append([brand.title(),
                              phone.find("div", {"class", "product-list__product-name"}).text.strip("\n"),
                              int(phone.find("span", {"class", "product-list__price"}).text.replace(".", "")),
                              int(phone.find("span", {"class", "score"})["style"].strip("width:%;"))/20])
    
    
phone_data = pd.DataFrame(allPhoneData, columns=['ProductBrand', 'ProductName', 'ProductPrice', 'ProductRate'])
phone_data.to_csv('vatanPhones.csv', index=False)
