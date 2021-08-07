import requests
import codecs
import json
from csv import reader
from tqdm import tqdm


def fetchDataFromPlacesAPI(Id, input):

    google_api_key = 'insert-googple-api-key-here'

    response = requests.get('https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input='+input +
                            '&inputtype=textquery&fields=formatted_address,name,opening_hours,rating,place_id&key='+google_api_key)
    place_search_json = response.json()

    try:
        place_id = place_search_json['candidates'][0]['place_id']
    except:
        return {}

    try:
        place_google_rating = place_search_json['candidates'][0]['rating']
    except:
        place_google_rating = ''

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
        place_area_jp = place_details_json['result']['address_components'][5]['long_name']
    except:
        place_area_jp = ''

    try:
        place_city_jp = place_details_json['result']['address_components'][6]['long_name']
    except:
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
        place_area_en = place_details_json_en['result']['address_components'][5]['long_name']
    except:
        place_area_en = ''

    try:
        place_city_en = place_details_json_en['result']['address_components'][6]['long_name']
    except:
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
        "Google_Rating": place_google_rating,
        "Use_Places_Data": 1
    }

    return result_dict


out_to_file = []

with tqdm(open('data/in/resto_identifier_all.csv', 'r')) as line:
    csv_reader = reader(line)
    for resto_name in csv_reader:
        out_to_file.append(fetchDataFromPlacesAPI(
            resto_name[0], resto_name[1]+'+'+resto_name[2]))

with codecs.open('data/out/place_details_all_prod.json', 'w', encoding='utf-8') as f:
    json.dump(out_to_file, f, ensure_ascii=False, indent=4)
