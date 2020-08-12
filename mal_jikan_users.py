import requests
import json

import pandas as pd
import  numpy as np

import time

"""
reference: https://jikan.docs.apiary.io/#reference/0/anime
"""

data = []

# col_names = ['user_id', 'anime_id','rating']

t = time.time()

"""
Data extracted from REST API
"""
friends_list = []

def get_friends(mal_user):
    global friends_list #To be able to append to global friends list
    frieds_url = f"https://api.jikan.moe/v3/user/{mal_user}/friends"
    friends_r = requests.get(frieds_url)

    if friends_r.ok:
        friends_json = friends_r.json()
        # print(json.dumps(friends_json, indent=2)) #pretty print

        print(f'Username: ', mal_user)

        page_loop = True
        page_num = 1
        friend_counter = 0
        friends_list = []

        while page_loop:

            print("\n Results from page ", page_num, "\n")
            frieds_url = f"https://api.jikan.moe/v3/user/{mal_user}/friends/{page_num}"
            friends_r = requests.get(frieds_url)
            friends_json = friends_r.json()

            for friend in friends_json['friends']:
                friends_list.append(friend['username'])
                print(f'User: ', friend['username'])

                friend_counter += 1
                print(f"friends counted: ",friend_counter)

            try:
                friends_json['friends'][99]
            except IndexError:
                page_loop = False
                return

            page_num += 1
            time.sleep(2)

        data.append(friends_list)

    else:
        print(f'{mal_user} has no friends :(')
        return

# Tests
# get_friends('Nekomata1037') #Has 36 friends
# get_friends('ysyouth') # has no friends :(
# get_friends('spacecowboy') #over 4,000 friends

new_df = pd.DataFrame(friends_list, columns=['users'])

df = pd.read_csv('../data/friends.csv')
df = df.append(new_df, ignore_index=True)

df.to_csv('../data/friends.csv', index=False)
friends_list.clear()
data.clear()
