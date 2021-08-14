# scripts
general purpose scripts

1(a). [fetch_places_data.py](https://github.com/gocurryjp/scripts/blob/master/scripts/fetch-places-data.py) -> to fetch data from Google Places API

    Pre-requisites :     
        - Set db creds
        - Set Google API key in the script
 
    
1(b). [insert_places_data.py](https://github.com/gocurryjp/scripts/blob/master/scripts/insert-places-data.py) -> to insert data fetched from Google Places API into the `place` table in the DB.  

    Pre-requisites :     
        - Set db creds
    
    
2. [newsfeed-batch.py](https://github.com/gocurryjp/scripts/blob/master/scripts/newsfeed-batch.py) -> to fetch fb posts and dump them to the gocurry db, to be run daily as a batch

    ```
    Pre-requisites : 
    - Log into Facebook and use a browser extension to download cookies.txt file
    - Put this file in the same directory as the script
    - set db creds
    - add pages to scrape to list at https://github.com/gocurryjp/scripts/blob/master/scripts/newsfeed-batch.py#L21
    ```
