# scripts
general purpose scripts

1. [fetch-places-data.py](https://github.com/gocurryjp/scripts/blob/master/scripts/fetch-places-data.py) -> to fetch data from Google Places API
    
    Pre-requisites : 
    - Dump latest restaurant id,restaurant name to CSV format from prod DB and store in data/in/resto_identifier_all.csv
    - Set Google API key in the script
2. [newsfeed-batch.py](https://github.com/gocurryjp/scripts/blob/master/scripts/newsfeed-batch.py) -> to fetch fb posts and dump them to the gocurry db, to be run daily as a batch
    
    Pre-requisites : 
    - Log into Facebook and use a browser extension to download cookies.txt file
    - Put this file in the same directory as the script
    - set db creds
    - add pages to scrape to the [list](https://github.com/gocurryjp/scripts/blob/master/scripts/newsfeed-batch.py#L21)
