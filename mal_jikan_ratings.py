import requests
import json

import pandas as pd
import  numpy as np

import time

"""
reference: https://jikan.docs.apiary.io/#reference/0/anime
"""

data = []

col_names = ['user_id', 'anime_id','rating']

t = time.time()

# Get detail information about user
# param = {'page':1, 'sort' : {'ordered_by': 'score'}}
# ratings_url = f"https://api.jikan.moe/v3/user/Nekomata1037/animelist/all?page=1&order_by=score&sort=desc"
ratings_url = f"https://api.jikan.moe/v3/user/ysyouth/animelist/all?page=1&order_by=score&sort=desc"

# This has a user id
user_url = f"https://api.jikan.moe/v3/user/ysyouth"


# Getting the review scores
# url = f"https://api.jikan.moe/v3/anime/{anime_id}/reviews"

user_r = requests.get(user_url)
user_json = user_r.json()

ratings_r = requests.get(ratings_url)
ratings_json = ratings_r.json()


# print(json.dumps(ratings_json, indent=2)) #pretty print
# print(json.dumps(user_json, indent=2)) #pretty print

"""
Data extracted from REST API
"""

print(f'Username: ', user_json['username'])

print(f'Username ID: ', user_json['user_id'])

for anime in ratings_json['anime']:
    print(f'Anime: ', anime['title'])

    print(f'Anime ID: ', anime['mal_id'])

    print(f'Rating for Anime: ', anime['score'])
