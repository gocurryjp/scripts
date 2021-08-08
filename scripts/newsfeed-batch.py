#!/usr/bin/python

from facebook_scraper import *
import sqlalchemy as db

from datetime import datetime

# log date/time of batch run
now = datetime.now()
print(now.strftime("%d/%m/%Y %H:%M:%S"))

# DB config
URL = 'localhost'
DB = 'gocurry'
USR = 'user'
PWD = 'password123'

SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@{}:3306/{}?charset=utf8mb4'.format(
    USR, PWD, URL, DB)

# Create connection to DB
engine = db.create_engine(SQLALCHEMY_DATABASE_URI)
connection = engine.connect()

# we will fetch data from gocurry's facebook page but also select restaurants with their permission
pages_list = [
    'gocurryjp',
    'NirvanamTokyo'
]

for page in pages_list:
    for post in get_posts(page, pages=1, cookies="/root/gocurry/cookies.txt"):
        if(page == 'gocurryjp'):
            isGoCurryPage = 1
        else:
            isGoCurryPage = 0

        query = "INSERT IGNORE INTO `newsfeed` (`id`, `source`, `username`, `body`, `url`, `image`, `images`, `external_link`, `likes`, `shares`, `video`, `video_thumbnail`, `is_live`, `is_gocurry_page`, `time`) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        data = (
            post['post_id'],
            'facebook',
            str(post['username']),
            str(post['post_text']),
            str(post['post_url']),
            str(post['image']),
            str(post['images']),
            str(post['link']),
            post['likes'],
            post['shares'],
            str(post['video']),
            str(post['video_thumbnail']),
            post['is_live'],
            isGoCurryPage,
            post['time']            
        )
        ResultProxy = connection.execute(query, data)
