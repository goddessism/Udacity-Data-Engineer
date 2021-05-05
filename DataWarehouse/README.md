Datawarehouse project for Sparkify
=============
----------------------------------------------
A music streaming startup, Sparkify's data engineer team has estalished a process for moving there data into redshift from S3 to continue to boost there analytics team's work.
This project is including a ETL pipeline for extracting there data from S3, stages them in Redshift, and transforms data into a set of dimensional tables.


----------------------------------------------
This project is consist of componects below.

Databasets 
-------------
You can work with 2 datasets such as logs, songs that resides in S3. 
- Song data: ```s3://udacity-dend/song_data``` 
- Log data: ```s3://udacity-dend/log_data```
- Log data json path: ```s3://udacity-dend/log_json_path.json```

Data Scheme 
-------------
- Staging Table
    - staging_events: Staging tabel for user activity data (like what songs are played?)
    - staging_songs: Staging table for song info data

- Fact Table
    - song_plays: records in event data associated with song plays i.e. records with page ```NextSong```
        - songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

- Dimension Table
    - users: users in the app
        - user_id, first_name, last_name, gender, level
    - songs: songs in music database
        - song_id, title, artist_id, year, duration
    - artists: artists in music database
        - artist_id, name, location, lattitude, longitude
    - time: timestamps of records in songplays broken down into specific units
        - start_time, hour, day, week, month, year, weekday

ETL pipeline
-------------
    1. Creating tables on Amazon Redshift to store the data from S3 buckets.
    2. Loading the data from S3 buckets to 2 staging tables on the Redshift Cluster.
    3. Insert data into the fact and dimension tables from staging tables.

How to run
------------- 
1. create tables
>$python ./create_tables.py

2. Run the etl pipeline
>$python ./etl.py

