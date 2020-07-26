import os
import psycopg2
from psycopg2 import Error

import numpy as np
import pandas as pd

import time

# https://pynative.com/python-postgresql-select-data-from-table/

def anime_query():
    t = time.time()
    try:
        # Connecting to PostgreSQL
        connection = psycopg2.connect(user = os.environ['PG_USER'],
                                      password = os.environ['POSTGRES_PASS'],
                                      host = "127.0.0.1",
                                      port = "5432",
                                      database = os.environ['PG_DB'])

        #
        cursor = connection.cursor()

        pg_query = """
        SELECT *
        FROM mal_anime
        """

        cursor.execute(pg_query)
        print("Selecting rows from anime table using cursor.fetchall")

        anime_data = np.array(cursor.fetchall())

        print(anime_data)
        print("Number of rows: ", len(anime_data,))
        print("Query completed in seconds: ", '{:0.2f}'.format(time.time()-t))
        return(anime_data)

    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching data from PostgreSQL: ", error)

    finally:
        #closing database connection.
            if(connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")

    print("Query completed in seconds: ", '{:0.2f}'.format(time.time()-t))

def ratings_query():
    t = time.time()
    try:
        # Connecting to PostgreSQL
        connection = psycopg2.connect(user = os.environ['PG_USER'],
                                      password = os.environ['POSTGRES_PASS'],
                                      host = "127.0.0.1",
                                      port = "5432",
                                      database = os.environ['PG_DB'])

        #
        cursor = connection.cursor()

        pg_query = """
        SELECT *
        FROM mal_ratings
        """

        cursor.execute(pg_query)
        print("Selecting rows from ratings table using cursor.fetchall")

        anime_data = np.array(cursor.fetchall())

        print(anime_data)
        print("Number of rows: ", len(anime_data,))
        print("Query completed in seconds: ", '{:0.2f}'.format(time.time()-t))
        return(anime_data)

    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching data from PostgreSQL: ", error)

    finally:
        #closing database connection.
            if(connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")

    print("Query completed in seconds: ", '{:0.2f}'.format(time.time()-t))

def merge_query():
    t = time.time()
    try:
        # Connecting to PostgreSQL
        connection = psycopg2.connect(user = os.environ['PG_USER'],
                                      password = os.environ['POSTGRES_PASS'],
                                      host = "127.0.0.1",
                                      port = "5432",
                                      database = os.environ['PG_DB'])

        #
        cursor = connection.cursor()

        pg_query = """
        SELECT *
        FROM merged_ratings
        """

        cursor.execute(pg_query)
        print("Selecting rows from anime table using cursor.fetchall")

        anime_data = np.array(cursor.fetchall())

        print(anime_data)
        print("Number of rows: ", len(anime_data,))
        print("Query completed in seconds: ", '{:0.2f}'.format(time.time()-t))
        return(anime_data)

    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching data from PostgreSQL: ", error)

    finally:
        #closing database connection.
            if(connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")

    print("Query completed in seconds: ", '{:0.2f}'.format(time.time()-t))

def merge_subset_query(anime_chosen):
    t = time.time()
    try:
        # Connecting to PostgreSQL
        connection = psycopg2.connect(user = os.environ['PG_USER'],
                                      password = os.environ['POSTGRES_PASS'],
                                      host = "127.0.0.1",
                                      port = "5432",
                                      database = os.environ['PG_DB'])

        #
        cursor = connection.cursor()

        pg_query = """
        WITH chosen_anime_users AS (
    	SELECT DISTINCT user_id
    	FROM merged_ratings
    	WHERE name = %s --Will use python to insert this
        )

        SELECT *
        FROM merged_ratings mr
        JOIN chosen_anime_users ca
        ON mr.user_id = ca.user_id
        WHERE mr.user_id = ca.user_id;
        """

        cursor.execute(pg_query, (str(anime_chosen),))
        print("Selecting rows from anime table using cursor.fetchall")

        anime_data = np.array(cursor.fetchall())

        print(anime_data)
        print("Number of rows: ", len(anime_data,))

        print("Query completed in seconds: ", '{:0.2f}'.format(time.time()-t))
        return(anime_data)

    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching data from PostgreSQL: ", error)

    finally:
        #closing database connection.
            if(connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")

    print("Query completed in seconds: ", '{:0.2f}'.format(time.time()-t))

# merge_subset_query('Mushishi')
# anime_query()
# ratings_query()
# merge_query()
