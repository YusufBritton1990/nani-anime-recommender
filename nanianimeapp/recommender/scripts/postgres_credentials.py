import os
import psycopg2
from psycopg2 import Error

import numpy as np
import pandas as pd

import time

# https://pynative.com/python-postgresql-select-data-from-table/
def pg_connection():
    connection = psycopg2.connect(user = os.environ['PG_USER'],
                              password = os.environ['POSTGRES_PASS'],
                              host = "127.0.0.1",
                              port = "5432",
                              database = os.environ['PG_DB'])
    return connection

def anime_query():
    pg_query = """
    SELECT *
    FROM recommender_mal_anime_prod
    WHERE anime_type = 'TV'
    """

    return pg_query

def ratings_query():
    pg_query = """
    SELECT *
    FROM recommender_mal_rating_prod
    """
    return pg_query

def merge_query():
    pg_query = """
    SELECT *
    FROM recommender_mal_merged_ratings_prod
    """

    return pg_query

def merge_refresh_query():
    pg_query = """
    DELETE FROM recommender_mal_merged_ratings_prod

    WITH mergedata AS (
    SELECT row_number() OVER() AS id,
    an.title_japanese,
    ra.rating,
    ra.anime_id_id,
    ra.user_id_id
    FROM recommender_mal_rating_prod AS ra
    LEFT JOIN recommender_mal_anime_prod AS an
    ON an.anime_id  = ra.anime_id_id
    WHERE an.members > 10000
    AND ra.rating > -1)

    INSERT INTO recommender_mal_merged_ratings_prod
    SELECT * FROM mergedata;
    """

    return pg_query


def merge_subset_query():
    pg_query = """
    WITH chosen_anime_users AS (
	SELECT DISTINCT user_id_id
	FROM recommender_mal_merged_ratings_prod
	WHERE anime_id_id = %(chosen_anime_id)s --Will use python to insert this
    )

    SELECT mr.*
    FROM recommender_mal_merged_ratings_prod mr
    JOIN chosen_anime_users ca
    ON mr.user_id_id = ca.user_id_id
    WHERE mr.user_id_id = ca.user_id_id;
    """

    return pg_query
