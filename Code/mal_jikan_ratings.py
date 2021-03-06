import requests
import json
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

import pandas as pd
import  numpy as np

import time
import datetime
import pytz #allows using tz classes to make UTC time usuable

"""
reference: https://jikan.docs.apiary.io/#reference/0/anime
"""

data = []

col_names = ['user_id', 'anime_id','rating']

t = time.time()

# print(json.dumps(ratings_json, indent=2)) #pretty print
# print(json.dumps(user_json, indent=2)) #pretty print

"""
Data extracted from REST API
"""

# 500 seconds with a 2 second rest over 16K ratings
def get_anime_rating(mal_user):
    time.sleep(4)

    user_url = f"https://api.jikan.moe/v3/user/{mal_user}"

    """In Case of 503 error, retry request"""
    s = requests.Session()

    retries = Retry(total=10,
            backoff_factor=4,
            status_forcelist=[503])

    s.mount('https://', HTTPAdapter(max_retries=retries))

    user_r = s.get(user_url)
    user_json = user_r.json()

    if user_r.status_code == 404:
        print(f'User {mal_user} does not exist')
        return

    print(f'Animes Watched: ', user_json['anime_stats']['total_entries'])
    print(f'Username: ', user_json['username'])
    print(f'Username ID: ', user_json['user_id'])

    # print(json.dumps(user_json, indent=2)) #pretty print
    page_loop = True
    page_num = 1

    while page_loop:
        time.sleep(4)
        print(f'Animes Watched: ', user_json['anime_stats']['total_entries'])
        print(f'Username: ', user_json['username'])
        print(f'Username ID: ', user_json['user_id'])

        if user_json['anime_stats']['total_entries'] == 0:
            print(f"Skipping {mal_user}, haven't watched any anime")
            page_loop = False
            return

        print("\n Results from page ", page_num, "\n")
        ratings_url = f"https://api.jikan.moe/v3/user/{mal_user}/animelist/all?page={page_num}&order_by=score&sort=desc"

        """In Case of 503 error, retry request"""
        s = requests.Session()

        retries = Retry(total=10,
                backoff_factor=4,
                status_forcelist=[503])

        s.mount('https://', HTTPAdapter(max_retries=retries))

        ratings_r = s.get(ratings_url)

        if ratings_r.status_code == 400:
            print(f'User {mal_user} anime list is restricted')
            page_loop = False
            return

        ratings_json = ratings_r.json()

        # print(json.dumps(ratings_json, indent=2)) #pretty print

        """Looping through a page of anime reviews"""
        for anime in ratings_json['anime']:
            global data
            rating_list = []
            # When a zero score is encounter, come out of function
            if anime['score'] == 0:
                page_loop = False
                return

            print(f'Anime: ', anime['title'])
            print(f'Anime ID: ', anime['mal_id'])
            print(f'Rating for Anime: ', anime['score'])

            # rating_list.append(anime['title'])
            rating_list.append(user_json['user_id'])
            rating_list.append(anime['mal_id'])
            rating_list.append(anime['score'])

            print('Saving at:', datetime.datetime.now(pytz.utc))
            rating_list.append(datetime.datetime.now(pytz.utc))

            print('Below is the list of rating data')
            print(rating_list)

            data.append(rating_list)

        """If there are more animes on the next page"""

        """Saving ratings after reading page"""
        new_df = pd.DataFrame(data, columns=col_names)

        df = pd.read_csv('../data/mal_ratings.csv')
        df = df.append(new_df, ignore_index=True)

        df.drop_duplicates(inplace=True)

        df.to_csv('../data/mal_ratings.csv', index=False)
        rating_list.clear()
        data.clear()

        """Checking to see if there are more pages"""
        try:
            ratings_json['anime'][299]
        except IndexError:
            page_loop = False
            return

        page_num += 1
        page_loop = False

"""User files"""
# Using friends file
# friends_df = pd.read_csv('../data/friends.csv')

# for index, mal_user in friends_df.users.items():
#     get_anime_rating(mal_user)

# Tests
# get_anime_rating('Nekomata1037') #One page of animes, many pages of zero
# get_anime_rating('ysyouth') #One page of animes, just two animes
# get_anime_rating('spacecowboy') #many animes
# get_anime_rating('lita4445') #restrict viewing their animes
# get_anime_rating('UnwaverRewaver')


"""Saving ratings"""
"""Appending user list"""
new_df = pd.DataFrame(data, columns=col_names)

df = pd.read_csv('../data/mal_ratings.csv')
df = df.append(new_df, ignore_index=True)

df.drop_duplicates(subset=['user_id', 'anime_id'], keep='last', inplace=True)

df.to_csv('../data/mal_ratings.csv', index=False)
data.clear()

print("Full run of code: ", '{:0.2f}'.format(time.time()-t))
