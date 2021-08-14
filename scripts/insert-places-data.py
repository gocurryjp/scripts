import json
import sqlalchemy as db

# read from places data file (json)
f = open('place_details_all_prod.json')
data = json.load(f)

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

for r in data:
    if r == {}:
        continue
    
    query = "INSERT IGNORE INTO `gocurry`.`place` (`Id`,`Name_JP`,`Name_EN`,`Address_JP`,`Address_EN`,`Area_JP`,`Area_EN`,`City_JP`,`City_EN`,`Latitude`,`Longitude`,`Timings_Text_JP0`,`Timings_Text_JP1`,`Timings_Text_JP2`,`Timings_Text_JP3`,`Timings_Text_JP4`,`Timings_Text_JP5`,`Timings_Text_JP6`,`Timings_Text_EN0`,`Timings_Text_EN1`,`Timings_Text_EN2`,`Timings_Text_EN3`,`Timings_Text_EN4`,`Timings_Text_EN5`,`Timings_Text_EN6`,`GMap_Url`,`Website`,`Place_id`,`Use_Places_Data`) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    data = (
        r['Id'],
        r['Name_JP'],
        r['Name_EN'],
        r['Address_JP'],
        r['Address_EN'],
        r['Area_JP'],
        r['Area_EN'],
        r['City_JP'],
        r['City_EN'],
        r['Latitude'],
        r['Longitude'],
        r['Timings_Text_JP'][0] if r['Timings_Text_JP'] else "",
        r['Timings_Text_JP'][1] if r['Timings_Text_JP'] else "",
        r['Timings_Text_JP'][2] if r['Timings_Text_JP'] else "",
        r['Timings_Text_JP'][3] if r['Timings_Text_JP'] else "",
        r['Timings_Text_JP'][4] if r['Timings_Text_JP'] else "",
        r['Timings_Text_JP'][5] if r['Timings_Text_JP'] else "",
        r['Timings_Text_JP'][6] if r['Timings_Text_JP'] else "",
        r['Timings_Text_EN'][0] if r['Timings_Text_EN'] else "",
        r['Timings_Text_EN'][1] if r['Timings_Text_EN'] else "",
        r['Timings_Text_EN'][2] if r['Timings_Text_EN'] else "",
        r['Timings_Text_EN'][3] if r['Timings_Text_EN'] else "",
        r['Timings_Text_EN'][4] if r['Timings_Text_EN'] else "",
        r['Timings_Text_EN'][5] if r['Timings_Text_EN'] else "",
        r['Timings_Text_EN'][6] if r['Timings_Text_EN'] else "",
        r['GMap_Url'],
        r['Website'],
        r['Place_id'],
        r['Use_Places_Data']            
    )
    
    ResultProxy = connection.execute(query, data)

# Closing file
f.close()