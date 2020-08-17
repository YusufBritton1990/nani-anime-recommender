import requests
import json
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

import pandas as pd
import  numpy as np

import time

"""
reference: https://jikan.docs.apiary.io/#reference/0/anime
"""

data = []

# TODO: Loop through initial list of users and get their friends
# col_names = ['user_id', 'anime_id','rating']

t = time.time()

"""
Data extracted from REST API
"""
friends_list = []

def get_friends(mal_user):
    # time.sleep(2)
    global friends_list #To be able to append to global friends list

    """This isn't needn't since we are not looping through users."""
    # frieds_url = f"https://api.jikan.moe/v3/user/{mal_user}/friends"
    # friends_r = requests.get(frieds_url)
    #
    # if friends_r.ok:
    #     friends_json = friends_r.json()
    #     print(json.dumps(friends_json, indent=2)) #pretty print
    #
    #     print(f'Username: ', mal_user)

    page_loop = True
    page_num = 1
    friend_counter = 0
    friends_list = []

    while page_loop:
        time.sleep(2)
        print(f'Username: ', mal_user)
        print("\n Results from page ", page_num, "\n")
        friends_url = f"https://api.jikan.moe/v3/user/{mal_user}/friends/{page_num}"

        """In Case of 503 error, retry request"""
        s = requests.Session()

        retries = Retry(total=10,
                backoff_factor=0.5,
                status_forcelist=[503])

        s.mount('https://', HTTPAdapter(max_retries=retries))


        # friends_r = requests.get(friends_url) #getting 503 error
        friends_r = s.get(friends_url)
        friends_json = friends_r.json()

        for friend in friends_json['friends']:
            friends_list.append(friend['username'])
            print(f'User: ', friend['username'])

            friend_counter += 1
            print(f"friends counted: ",friend_counter)

        """Exceptions"""

        # Checking to see if there are more friends on the page
        try:
            friends_json['friends'][99]
        except IndexError:
            page_loop = False
            return

        # If increment of 100, come out of the function
        try:
            friends_json['friends'][0]
        except IndexError:
            page_loop = False
            return

        """Go to the next page"""
        page_num += 1

    else:
        print(f'{mal_user} has no friends :(')
        return

# Tests
# get_friends('Nekomata1037') #Has 36 friends
# get_friends('ysyouth') # has no friends :(
# get_friends('spacecowboy') #over 4,000 friends
# get_friends('BobSamurai') #over 1,500
# get_friends('etekusat') #over 6,000


"""Appending user list"""
new_df = pd.DataFrame(friends_list, columns=['users'])

df = pd.read_csv('../data/friends.csv')
df = df.append(new_df, ignore_index=True)

df.drop_duplicates(inplace=True)

df.to_csv('../data/friends.csv', index=False)
friends_list.clear()
data.clear()
