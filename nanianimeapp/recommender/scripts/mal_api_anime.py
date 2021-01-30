import requests
import json

import pandas as pd
import  numpy as np

import time
import datetime
import pytz #allows using tz classes to make UTC time usuable

"""
reference:
https://myanimelist.net/apiconfig/references/api/v2#operation/anime_anime_id_get
"""

def get_anime(first_anime_id, last_anime_id,access_token):
    """
    Based on anime id selection, makes an API call to MAL.
    Need authorization in order to call

    fields retrieved:
    id,title,main_picture,alternative_titles,
    start_date,end_date,synopsis,mean,rank,popularity,
    num_list_users,num_scoring_users,nsfw,created_at,
    updated_at,media_type,status,genres,my_list_status,
    num_episodes,start_season,broadcast,source,
    average_episode_duration,rating,pictures,
    background,related_anime,related_manga,
    recommendations,studios,statistics
    """

    bad_ids_list = []
    data = []

    t = time.time()
    for anime_id in range(first_anime_id, last_anime_id+1):

        try:
            # Get detail information about anime
            base_url = f"https://api.myanimelist.net/v2/anime/{anime_id}"

            fields = """fields=id,title,main_picture,alternative_titles,
            start_date,end_date,synopsis,mean,rank,popularity,
            num_list_users,num_scoring_users,nsfw,created_at,
            updated_at,media_type,status,genres,my_list_status,
            num_episodes,start_season,broadcast,source,
            average_episode_duration,rating,pictures,
            background,related_anime,related_manga,
            recommendations,studios,statistics"""

            url = f"{base_url}?{fields}"

            r = requests.get(url, headers={'Authorization': f'Bearer {access_token}'})
            anime_json = r.json()
            # print(json.dumps(anime_json, indent=2)) #pretty print

            data.append(anime_json)
            time.sleep(2)

        # TODO: Need to capture error log somewhere
        except requests.exceptions.RequestException as e:
            print(f'Issue with requesting Anime ID {anime_id}, error: {e}')
            bad_ids.append(anime_id)
            # time.sleep(4)
            continue

        except KeyError:
            print(f'Anime ID {anime_id} does not exist')
            print('Saving at:', datetime.datetime.now(pytz.utc))

            bad_ids_list.append(anime_id, datetime.datetime.now(pytz.utc))
            # time.sleep(4)
            continue
    print("Full run of code: ", '{:0.2f}'.format(time.time()-t))
    return data

# Testing
# mushishi_id = 457

# print('Number of entries: ', len(data))
# print(anime_dict)

# Updating SQL
# get_anime(1,1)

# Updating excel sheet
# new_df = pd.DataFrame(data, columns = col_names)
# new_bad_ids_df = pd.DataFrame(bad_ids_list, columns = ['anime_id'])
#
# df = pd.read_csv('../data/example.csv')
# bad_ids_df = pd.read_csv('../data/bad_ids.csv')
#
# df = df.append(new_df, ignore_index=True)
# bad_ids_df = bad_ids_df.append(new_bad_ids_df, ignore_index=True)
#
# df.drop_duplicates(subset='anime_id', keep='last', inplace=True)
# bad_ids_df.drop_duplicates(subset='anime_id', keep="last", inplace=True)
#
# # print(df)
# df.to_csv('../data/example.csv', index=False)
# bad_ids_df.to_csv('../data/bad_ids.csv', index=False)

# TODO: During periodic update, build logic in chronjob
# Save data periodically, in case script is interuptted
# if anime_id % 50 == 0:
#
#     new_df = pd.DataFrame(data, columns = col_names)
#     new_bad_ids_df = pd.DataFrame(bad_ids_list, columns = ['anime_id']
#
#     df = pd.read_csv('../data/example.csv')
#     bad_ids_df = pd.read_csv('../data/bad_ids.csv')
#
#     df = df.append(new_df, ignore_index=True)
#     bad_ids_df = bad_ids_df.append(new_bad_ids_df, ignore_index=True)
#
#     df.drop_duplicates(inplace=True)
#     bad_ids_df.drop_duplicates(inplace=True)
#
#     # print(df)
#     df.to_csv('../data/example.csv', index=False)
#     bad_ids_df.to_csv('../data/bad_ids.csv', index=False)
#
#     bad_ids_list.clear()
#     data.clear()
