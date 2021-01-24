ETL Project for Sparkify
=============
----------------------------------------------
Sparkify team is now loading json files with their songs infromation data and log data.
They want to prepare a new method to search quickly and analyze smoothly even the data become more bigger. 
This project is designed to accomplish the goal with codes.
Introduction
=============
----------------------------------------------
This ETL pipeline project is consist of componects below.

Database tables 
-------------
- Structure

    - All datasets are organized with STAR scheme including one fact table (song_play) and 4 dimension tables (users, songs, artists, time). This can solve business requirement like below
    - What is the next song users would like to play based on what songs they have listened past.
    - When users listen each song based on song have played point of time and what season.

- Utilization - This database will be utilized various scenes like below.
    - Songs suggestions #1: Sparkify can offer song suggestions such as /gender /recently played songs.
    - Grouping users : Can make group by pattern for song played and Utilize it to Songs or Artists suggestion. 
    - Most played songs on each season (or year or month) : Users can check and listen most played songs with aleady made song lists automatically.

ETL pipeline
-------------
- sql_queries.py : This python file contains all queries for this ETL pipeline.
- create_table.py : This python control all of drop and create table logic. You have to execute this file when you need to initialize table or data.
- run following command to initialize table and data before executing pipeline.
1. create_tables.py
```$ python create_tables.py```   
2. etl.py
```$ python etl.py```
3. test.ipynb (on notebook)

- etl.py : 
    - ETL pipeline Create songs and artists table and insert data with selected columns of song_data from json files on /song_data.
    - ETL pipeline Create time and users table and insert data with selected columns of log_data from json files on /log_data.
    - ETL pipeline create song_play table and insert data from song_data and log_data.

Notebooks for test
-------------
- test.py : To check results of executing etl.py or etl.ipynb file.
- etl.ipynb : To try and modify ETL logic of etl.py  This notebook has logic for only 1 record to check behavior of the pipeline and detailed instructions for developing ETL process with etl.py. 

