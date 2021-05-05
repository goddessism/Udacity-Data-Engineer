import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= ("""
CREATE TABLE staging_events(
    artist_name VARCHAR(256),
    auth VARCHAR(16),
    first_name VARCHAR(256),
    gender  VARCHAR(1),
    item_in_session	INTEGER,
    last_name VARCHAR(256),
    song_length DOUBLE PRECISION, 
    level VARCHAR(8),
    location VARCHAR(256),	
    method VARCHAR(8),
    page VARCHAR(16),	
    registration BIGINT,	
    session_id	INT,
    song_title VARCHAR(256),
    status INTEGER, 
    ts VARCHAR(50),
    user_agent TEXT,	
    user_id VARCHAR(64)
);
""")

staging_songs_table_create = ("""
CREATE TABLE staging_songs(
    num_songs INTEGER,
    artist_id VARCHAR(32),
    artist_latitude DOUBLE PRECISION,
    artist_longitude DOUBLE PRECISION,
    artist_location VARCHAR(256),
    artist_name VARCHAR(256),
    song_id VARCHAR(32),    
    title VARCHAR(256),
    duration DOUBLE PRECISION,
    year INTEGER
);
""")

songplay_table_create = ("""
CREATE TABLE songplays(
    songplay_id INT IDENTITY(0,1) PRIMARY KEY,
    start_time TIMESTAMP NOT NULL,
    user_id VARCHAR(64) NOT NULL,
    level VARCHAR(8),
    song_id VARCHAR(32) NOT NULL,
    artist_id VARCHAR(32) NOT NULL,
    session_id INT NOT NULL,
    location VARCHAR(256) NOT NULL,
    user_agent TEXT
)
DISTSTYLE KEY
DISTKEY ( start_time )
SORTKEY ( start_time );
""")

user_table_create = ("""
CREATE TABLE users(
    user_id VARCHAR(64) PRIMARY KEY,
    first_name VARCHAR(256) NOT NULL,
    last_name VARCHAR(256) NOT NULL,
    gender VARCHAR(1) NOT NULL,
    level VARCHAR(8) NOT NULL
)
DISTSTYLE ALL
SORTKEY ( user_id );
""")

song_table_create = ("""
CREATE TABLE songs(
    song_id VARCHAR(32) NOT NULL PRIMARY KEY,
    title VARCHAR(256) NOT NULL,
    artist_id VARCHAR(32) NOT NULL,
    year INTEGER NOT NULL,
    duration DOUBLE PRECISION NOT NULL
)
DISTSTYLE ALL
SORTKEY ( song_id );
""")

artist_table_create = ("""
CREATE TABLE artists(
    artist_id VARCHAR(32) NOT NULL PRIMARY KEY,
    name VARCHAR(256) NOT NULL,
    location VARCHAR(256),
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION
)
DISTSTYLE ALL
SORTKEY ( artist_id );
""")

time_table_create = ("""
CREATE TABLE time(
    start_time TIMESTAMP NOT NULL PRIMARY KEY,
    hour INTEGER NOT NULL,
    day INTEGER NOT NULL,
    week INTEGER NOT NULL,
    month INTEGER NOT NULL,
    year INTEGER NOT NULL,
    weekday INTEGER NOT NULL
)
DISTSTYLE KEY
DISTKEY ( start_time )
SORTKEY ( start_time );
""")

# STAGING TABLES

staging_events_copy = ("""
COPY staging_events 
FROM {}
IAM_ROLE {}
JSON {};
                       """).format(config.get('S3','LOG_DATA'), config.get('IAM_ROLE', 'ARN'), config.get('S3','LOG_JSONPATH'))

staging_songs_copy = ("""
COPY staging_songs 
FROM {} 
IAM_ROLE {}
JSON 'auto';
                      """).format(config.get('S3','SONG_DATA'), config.get('IAM_ROLE', 'ARN'))

# FINAL TABLES

songplay_table_insert = ("""
INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent) 
SELECT  
    TIMESTAMP 'epoch' + e.ts/1000 * interval '1 second' as start_time, 
    e.user_id, 
    e.level, 
    s.song_id,
    s.artist_id, 
    e.session_id,
    e.location, 
    e.user_agent
FROM staging_events e, staging_songs s
WHERE e.page = 'NextSong' 
AND e.song_title = s.title 
AND e.artist_name = s.artist_name 
AND e.song_length = s.duration
""")

user_table_insert = ("""
INSERT INTO users (user_id, first_name, last_name, gender, level)
SELECT DISTINCT  
    user_id, 
    first_name, 
    last_name, 
    gender, 
    level
FROM staging_events
WHERE page = 'NextSong'
""")

song_table_insert = ("""
INSERT INTO songs (song_id, title, artist_id, year, duration) 
SELECT DISTINCT 
    song_id, 
    title,
    artist_id,
    year,
    duration
FROM staging_songs
WHERE song_id IS NOT NULL
""")

artist_table_insert = ("""
INSERT INTO artists (artist_id, name, location, latitude, longitude) 
SELECT DISTINCT 
    artist_id,
    artist_name,
    artist_location,
    artist_latitude,
    artist_longitude
FROM staging_songs
WHERE artist_id IS NOT NULL
""")

time_table_insert = ("""
INSERT INTO time(start_time, hour, day, week, month, year, weekDay)
SELECT start_time, 
    extract(hour from start_time),
    extract(day from start_time),
    extract(week from start_time), 
    extract(month from start_time),
    extract(year from start_time), 
    extract(dayofweek from start_time)
FROM songplays
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
