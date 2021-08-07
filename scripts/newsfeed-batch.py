#!/usr/bin/python

from facebook_scraper import *
import sqlalchemy as db

# DB config
URL = 'localhost'
DB = 'gocurry'
USR = 'user'
PWD = 'password'

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

        query = "INSERT IGNORE INTO  `news_feed` (`post_id`, `post_text`, `post_url`, `username`, `time`, `is_gocurry_page`, `source`, `likes`) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"

        data = (
            post['post_id'],
            str(post['post_text']),
            post['post_url'],
            str(post['username']),
            post['time'],
            isGoCurryPage,
            'facebook',
            post['likes']
        )
        ResultProxy = connection.execute(query, data)
