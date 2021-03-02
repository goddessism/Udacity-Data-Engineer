Cassandra ETL Project for Sparkify
=============
----------------------------------------------
Sparkify team is now loading csv files with user activity data especially focusing played songs by each session.
- Goal : 
    - Analytics team can gather user list by each specific song.  
    - Can gather song's information by session and play number key.
    - Can gather artist and song information by specific user who has played. 
This project is designed to accomplish the goal with codes.

Introduction
=============
----------------------------------------------
This notebook is consist of componects below.

Database tables 
-------------
- Structure

    - event_data : Csv files with user activity data provide what you want to refine.
    - Project_1B_ Project_Template.ipynb : This file is a notebook for ETL source code and a hero of this project.
    - event_datafile_new.csv : Refined data for mapping to insert query. Refining is conducted with csv files in /event_data.
    - images : Sample image for Understanding what structure is required for making event_datafile_new.csv
    - README.md : Introduction for this project
