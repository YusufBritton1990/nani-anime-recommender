import requests
import json

"""
reference: https://jikan.docs.apiary.io/#reference/0/anime
"""

mushishi_id = 457

# f"https://api.jikan.moe/v3/anime/{id}(/request)"

url = f"https://api.jikan.moe/v3/anime/{mushishi_id}"
r = requests.get(url)

anime_json = r.json()

# print(json.dumps(anime_json, indent=2)) #pretty print

"""
Data extracted from REST API
"""
# Name of anime
print("Name of anime: ",anime_json['title'])

# Cover art (store actual images in aws)
print("URL to Cover Picture: ",anime_json['image_url'])

# Type
print("Type: ",anime_json['type'])

# Genres
for i in range(len(anime_json['genres'])):
    print("Genre: ",anime_json['genres'][i]['name'])

# Episode
print("Episodes: ",anime_json['episodes'])

# Link to MAL
print("URL to MAL: ",anime_json['url'])

# Synopsis
print("Synopsis: ",anime_json['synopsis'])

# Youtube link
print("URL to Trailer: ",anime_json['trailer_url'])


# Overall Rating
print("Overall Rating: ",anime_json['score'])
print("Amount of ratings: ",anime_json['scored_by'])

# Rating from members
