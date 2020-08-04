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
param = {'page':1, 'sort' : {'ordered_by': 'score'}}
url = f"https://api.jikan.moe/v3/user/Nekomata1037/animelist/all?page=1&order_by=score&sort=desc"
# url = f"https://api.jikan.moe/v3/user/ysyouth/animelist/all?page=1&order_by=score&sort=desc"

# Getting the review scores
# url = f"https://api.jikan.moe/v3/anime/{anime_id}/reviews"

r = requests.get(url)
rating_json = r.json()

print(json.dumps(rating_json, indent=2)) #pretty print

"""
Data extracted from REST API
"""
