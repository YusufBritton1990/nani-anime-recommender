import requests
import json

import pandas as pd
import  numpy as np

import time

"""
reference: https://jikan.docs.apiary.io/#reference/0/anime
"""

bad_ids_list = []
data = []
# mushishi_id = 457

col_names = ['anime_id', 'title_japanese', 'title_english', 'image_url',
            'anime_type', 'genres', 'episodes', 'mal_url', 'synopsis',
            'trailer_url','rating', 'members']

# Takes about 8 hours to look up 20K entries
first_anime_id = 44399
last_anime_id = 45000

t = time.time()
for anime_id in range(first_anime_id, last_anime_id+1):

    # Save data periodically, in case script is interuptted
    if anime_id % 50 == 0:

        new_df = pd.DataFrame(data, columns = col_names)
        new_bad_ids_df = pd.DataFrame(bad_ids_list, columns = ['anime_id'])

        df = pd.read_csv('../data/example.csv')
        bad_ids_df = pd.read_csv('../data/bad_ids.csv')

        df = df.append(new_df, ignore_index=True)
        bad_ids_df = bad_ids_df.append(new_bad_ids_df, ignore_index=True)

        df.drop_duplicates(inplace=True)
        bad_ids_df.drop_duplicates(inplace=True)

        # print(df)
        df.to_csv('../data/example.csv', index=False)
        bad_ids_df.to_csv('../data/bad_ids.csv', index=False)

        bad_ids_list.clear()
        data.clear()

    try:
        # f"https://api.jikan.moe/v3/anime/{id}(/request)"

        # Get detail information about anime
        url = f"https://api.jikan.moe/v3/anime/{anime_id}"

        # Getting the review scores
        # url = f"https://api.jikan.moe/v3/anime/{anime_id}/reviews"

        r = requests.get(url)
        anime_json = r.json()

        # print(json.dumps(anime_json, indent=2)) #pretty print

        """
        Data extracted from REST API
        """

        anime_list = []
        # Anime id
        anime_list.append(anime_json['mal_id'])
        print("ID of Anime: ",anime_json['mal_id'])

        # Name of anime
        anime_list.append(anime_json['title'])
        print("Name of anime (Japanese): ",anime_json['title'])

        anime_list.append(anime_json['title_english'])
        print("Name of anime (English): ",anime_json['title_english'])

        # Cover art (store actual images in aws)
        anime_list.append(anime_json['image_url'])
        print("URL to Cover Picture: ",anime_json['image_url'])

        # Type
        anime_list.append(anime_json['type'])
        print("Type: ",anime_json['type'])

        # Genres
        genre_list = []
        for genre in anime_json['genres']:
            genre_list.append(genre['name'])
            print("Genre: ", genre['name'])

        genre_list = ', '.join(genre_list)
        anime_list.append(genre_list)

        # Episode
        anime_list.append(anime_json['episodes'])
        print("Episodes: ",anime_json['episodes'])


        # Link to MAL
        anime_list.append(anime_json['url'])
        print("URL to MAL: ",anime_json['url'])

        # Synopsis
        anime_list.append(anime_json['synopsis'])
        try:
            print("Synopsis: ",anime_json['synopsis'][0:50])
        except TypeError:
            print("Synopsis: None")

        # Youtube link
        anime_list.append(anime_json['trailer_url'])
        print("URL to Trailer: ",anime_json['trailer_url'])


        # Overall Rating
        anime_list.append(anime_json['score'])
        print("Overall Rating: ",anime_json['score'])

        anime_list.append(anime_json['scored_by'])
        print("Amount of ratings: ",anime_json['scored_by'])

        # TODO: Will leave this for now
        # Rating from members

        # print('Number of columns: ', len(col_names))
        # print('Number of entries: ', len(anime_list))

        data.append(anime_list)
        time.sleep(2)

    except requests.exceptions.RequestException as e:
        print(f'Issue with requesting Anime ID {anime_id}, error: {e}')
        bad_ids.append(anime_id)
        # time.sleep(4)
        continue

    except KeyError:
        print(f'Anime ID {anime_id} does not exist')
        bad_ids_list.append(anime_id)
        # time.sleep(4)
        continue

# print('Number of entries: ', len(data))
# print(anime_list)
new_df = pd.DataFrame(data, columns = col_names)
new_bad_ids_df = pd.DataFrame(bad_ids_list, columns = ['anime_id'])

df = pd.read_csv('../data/example.csv')
bad_ids_df = pd.read_csv('../data/bad_ids.csv')

df = df.append(new_df, ignore_index=True)
bad_ids_df = bad_ids_df.append(new_bad_ids_df, ignore_index=True)

df.drop_duplicates(inplace=True)
bad_ids_df.drop_duplicates(inplace=True)

# print(df)
df.to_csv('../data/example.csv', index=False)
bad_ids_df.to_csv('../data/bad_ids.csv', index=False)

print("Full run of code: ", '{:0.2f}'.format(time.time()-t))
