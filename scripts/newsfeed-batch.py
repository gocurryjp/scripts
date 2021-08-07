#!/usr/bin/python

# -*- coding: utf-8 -*-

from facebook_scraper import *
import sqlalchemy as db

# DB config
URL='localhost'
DB='gocurry'
USR='root'
PWD='password'

SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@{}:3306/{}'.format(USR, PWD,URL,DB)

# Create connection to DB
engine = db.create_engine(SQLALCHEMY_DATABASE_URI) 
connection = engine.connect()

# we will fetch data from gocurry's facebook page but also select restaurants with their permission
pages_list = [
    'gocurryjp',
    'NirvanamTokyo'
]

for page in pages_list:
    for post in get_posts(page, pages=1, cookies="cookies.txt", encoding='utf-8'):
        
        if(page == 'gocurryjp'):
            isGoCurryPage = 1
        else:
            isGoCurryPage = 0

        query = "INSERT IGNORE INTO  `news_feed` (`post_id`, `post_text`, `post_url`, `username`, `time`, `is_gocurry_page`, `source`, `likes`) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"

        data = (
            post['post_id'], 
            post['post_text'].encode('utf8'), 
            post['post_url'], 
            post['username'], 
            post['time'], 
            isGoCurryPage,
            'facebook',
            post['likes']
        )    

        ResultProxy = connection.execute(query,data)