import requests
import json
from geopy.geocoders import Nominatim
from scraper_api import ScraperAPIClient
import time
import aiohttp
import asyncio

client = ScraperAPIClient('b84eb72339700a4b47310d5fae46e41b')

p_location = input("Enter location: ")
p_size = int(input("Enter size: "))
#search_range = float(input("Enter the range of your search: "))

start_time = time.time()

geolocator = Nominatim(user_agent="MenShoesBershka.py")
location = geolocator.geocode(p_location)
print((location.latitude, location.longitude))

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}

location_around_user = requests.get("https://www.bershka.com/itxrest/2/bam/store/44009506/physical-store?latitude=51.5073219&longitude=-0.1276474&countryCode=GB&max=10&appId=2&languageId=-1", headers=headers).json()

store_ids = []

x = 0

while x < len(location_around_user["closerStores"]):
    print(location_around_user["closerStores"][x]["id"]+", "+location_around_user["closerStores"][x]["name"])
    store_ids.append(location_around_user["closerStores"][x]["id"])
    x = x+1

products = requests.get("https://www.bershka.com/itxrest/2/catalog/store/44009506/40259534/category/1010193202/product?languageId=-1", headers=headers).json()

i = 0

p_pn = []

while i < len(products["products"]):
    try:
        p_pn.append(products["products"][i]["bundleProductSummaries"][0]["detail"]["colors"][0]["sizes"][0]["partnumber"][0:13])
        print(p_pn[i]+" ", i+1)
        i=i+1
    except IndexError:
        break
    

list(dict.fromkeys(p_pn))
i=0

print("check")

while i < len(p_pn):
    try:
        p_stock = requests.get("https://itxrest.inditex.com/LOMOServiciosRESTCommerce-ws/common/1/stock/campaign/V2021/product/part-number/"+p_pn[i]+"?physicalStoreId="+store_ids[0]+"&physicalStoreId="+store_ids[1]+"&physicalStoreId="+store_ids[2], headers=headers).json()
        counter = 0
        print("Product: #"+p_pn[i])
        if len(p_stock["stocks"]) == 0:
            print("product not available in stores around you.")
        else:
            while counter < len(p_stock["stocks"]):
                if not any(d["size"] == (34+p_size) for d in p_stock["stocks"][counter]["sizeStocks"]):
                    print("This store doesn't have your size: "+str(p_stock["stocks"][counter]["physicalStoreId"]))
                    # does not exist
                else:
                    print("Available at: "+str(p_stock["stocks"][counter]["physicalStoreId"]))
                counter = counter + 1
    except ValueError:
        print("product not available in stores around you")
    finally:
        i=i+1

print("the end")
print("Process finished --- %s seconds ---" % round((time.time() - start_time),2))
