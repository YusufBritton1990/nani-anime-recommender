import requests
import json

import pandas as pd
import  numpy as np

import time

"""
reference: https://jikan.docs.apiary.io/#reference/0/anime
"""

# data = []

# col_names = ['user_id', 'anime_id','rating']

# TODO: Need to be able to call next page

t = time.time()

"""
Data extracted from REST API
"""

def get_anime_rating(mal_user):
    user_url = f"https://api.jikan.moe/v3/user/{mal_user}"
    user_r = requests.get(user_url)
    user_json = user_r.json()

    print(f'Animes Watched: ', user_json['username'])
    print(f'Username: ', user_json['username'])
    print(f'Username ID: ', user_json['user_id'])

    page_loop = True
    page_num = 1

    while page_loop:
        print("\n Results from page ", page_num, "\n")
        ratings_url = f"https://api.jikan.moe/v3/user/{mal_user}/animelist/all?page={page_num}&order_by=score&sort=desc"
        ratings_r = requests.get(ratings_url)
        ratings_json = ratings_r.json()

        for anime in ratings_json['anime']:
            # When a zero score is encounter, come out of function
            if anime['score'] == 0:
                page_loop = False
                return

            print(f'Anime: ', anime['title'])
            print(f'Anime ID: ', anime['mal_id'])
            print(f'Rating for Anime: ', anime['score'])

        try:
            ratings_json['anime'][299]
        except IndexError:
            page_loop = False
            return

        page_num += 1
        time.sleep(2)

        # print(json.dumps(ratings_json, indent=2)) #pretty print
        # print(json.dumps(user_json, indent=2)) #pretty print

# Tests
# get_anime_rating('Nekomata1037') #One page of animes, many pages of zero
# get_anime_rating('ysyouth') #One page of animes, just two animes
# get_anime_rating('spacecowboy') #many animes
