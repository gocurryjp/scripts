import requests
import codecs
import json
import sqlalchemy as db

# Method to fetch data from Places API

def fetchDataFromPlacesAPI(Id, search_input):

    google_api_key = 'insert-google-api-key'

    response = requests.get('https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input='+search_input +
                            '&inputtype=textquery&fields=formatted_address,name,opening_hours,place_id&key='+google_api_key)
    place_search_json = response.json()

    try:
        place_id = place_search_json['candidates'][0]['place_id']
    except:
        return {}

    response = requests.get('https://maps.googleapis.com/maps/api/place/details/json?place_id='+place_id +
                            '&fields=name,address_component,formatted_address,geometry/location,opening_hours,website,price_level,url&language=ja&key='+google_api_key)

    place_details_json = response.json()

    try:
        place_name_jp = place_details_json['result']['name']
    except:
        place_name_jp = ''

    try:
        place_address_jp = place_details_json['result']['formatted_address']
    except:
        place_address_jp = ''

    try:
        place_area_jp = ''
        place_city_jp = ''
        address_json = place_details_json['result']['address_components']

        for address in address_json:
            if("sublocality_level_2" in address['types']):
                place_area_jp = address['long_name']    

            if("locality" in address['types']):
                place_city_jp = address['long_name']
    except:
        place_area_jp = ''
        place_city_jp = ''
    
    try:
        place_lat = place_details_json['result']['geometry']['location']['lat']
    except:
        place_lat = ''

    try:
        place_lng = place_details_json['result']['geometry']['location']['lng']
    except:
        place_lng = ''

    try:
        place_opening_hours = place_details_json['result']['opening_hours']['weekday_text']
    except:
        place_opening_hours = ''

    try:
        place_gmap_url = place_details_json['result']['url']
    except:
        place_gmap_url = ''

    try:
        place_website = place_details_json['result']['website']
    except:
        place_website = ''

    response = requests.get('https://maps.googleapis.com/maps/api/place/details/json?place_id='+place_id +
                            '&fields=name,address_component,opening_hours,formatted_address&language=en&key='+google_api_key)

    place_details_json_en = response.json()

    try:
        place_name_en = place_details_json_en['result']['name']
    except:
        place_name_en = ''

    try:
        place_address_en = place_details_json_en['result']['formatted_address']
    except:
        place_address_en = ''

    try:
        place_area_en = ''
        place_city_en = ''
        address_en_json = place_details_json_en['result']['address_components']

        for address in address_en_json:
            if("sublocality_level_2" in address['types']):
                place_area_en = address['long_name']    

            if("locality" in address['types']):
                place_city_en = address['long_name']
    except:
        place_area_en = ''
        place_city_en = ''

    try:
        place_opening_hours_en = place_details_json_en['result']['opening_hours']['weekday_text']
    except:
        place_opening_hours_en = ''

    result_dict = {
        "Id": Id,
        "Place_id": place_id,
        "Name_JP": place_name_jp,
        "Name_EN": place_name_en,
        "Address_JP": place_address_jp,
        "Address_EN": place_address_en,
        "Area_JP": place_area_jp,
        "Area_EN": place_area_en,
        "City_JP": place_city_jp,
        "City_EN": place_city_en,
        "Latitude": place_lat,
        "Longitude": place_lng,
        "Timings_Text_JP": place_opening_hours,
        "Timings_Text_EN": place_opening_hours_en,
        "GMap_Url": place_gmap_url,
        "Website": place_website,        
        "Use_Places_Data": 1
    }

    return result_dict

#
#
#

# Main script

# DB config
URL = 'localhost'
DB = 'gocurry'
USR = 'root'
PWD = 'password'

SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@{}:3306/{}?charset=utf8mb4'.format(
    USR, PWD, URL, DB)

# Create connection to DB
engine = db.create_engine(SQLALCHEMY_DATABASE_URI)
connection = engine.connect()

# Fetch all restaurants from the DB
query = "SELECT Id,Name_Japanese,Area FROM gocurry.restaurant"
    
restaurant_info = connection.execute(query)

out_to_file = []

for resto_data in restaurant_info:
    print("Fetch place details for "+resto_data.Name_Japanese)
    out_to_file.append(fetchDataFromPlacesAPI(resto_data.Id,resto_data.Name_Japanese+"+"+resto_data.Area))

with codecs.open('place_details_all_prod.json', 'w', encoding='utf-8') as f:
    json.dump(out_to_file, f, ensure_ascii=False, indent=4)
