import postgres_credentials as pg

import time

# Look into this later
# from sklearn.preprocessing import StandardScaler
# from sklearn.decomposition import PCA
# from sklearn.cluster import KMeans
# from sklearn.metrics import silhouette_score


import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# sns.set_style('whitegrid')
# %matplotlib inline #Used in jupyter notebook

start = time.time()


"""Assigning Dataframes"""

print('Querying Animes')
# rating_df = pd.read_sql_query(pg.ratings_query(),pg.pg_connection())
anime_df = pd.read_sql_query(pg.anime_query(),pg.pg_connection())
# merged_df = pd.read_sql_query(pg.merge_query(),pg.pg_connection())
print('Completed in: ', '{:0.2f}'.format(time.time()-start))

chosen_anime = 'Hajime no Ippo'
param = {'anime' : chosen_anime}

print('Querying subset for: ', chosen_anime)
user_subset_df = pd.read_sql_query(pg.merge_subset_query(),
                    pg.pg_connection(), params=param)
print('Completed in: ', '{:0.2f}'.format(time.time()-start))

"""Creating relationship tables"""
# Construct average scores of animes
rating_mean_df = pd.DataFrame(user_subset_df.groupby('name')['rating'].mean())
rating_mean_df['num of ratings'] = pd.DataFrame(user_subset_df.groupby('name')['rating'].count())

# Pic the genres from this selection
genre_dict = pd.DataFrame(data=anime_df[['name','genre']])
genre_dict.set_index('name',inplace=True) #This is what is ingested

"""Recommendation functions"""
def check_genre(genre_list,string):
    if any(x in string for x in genre_list):
        return True
    else:
        return False

# TODO: When looking a anime with a small poll of viewing, dynamically update ['num of ratings']
def get_recommendation(name):
    #generating list of anime with the same genre with target
    anime_genre = genre_dict.loc[name].values[0].split(', ') #
    cols = anime_df[anime_df['genre'].apply(
        lambda x: check_genre(anime_genre,str(x)))]['name'].tolist()

    #create matrix based on generated list
    animemat = user_subset_df[user_subset_df['name'].isin(cols)].pivot_table(
        index='user_id',columns='name',values='rating')

    #create correlation table
    anime_user_rating = animemat[name]
    similiar_anime = animemat.corrwith(anime_user_rating)
    corr_anime = pd.DataFrame(similiar_anime,columns=['correlation'])
    corr_anime = corr_anime.join(rating_mean_df['num of ratings'])
    corr_anime.dropna(inplace=True)
    corr_anime = corr_anime[corr_anime['num of ratings'] > 1000].sort_values(
        'correlation',ascending=False)

    return corr_anime.head(10)

# Test
print('Gathering Recommendations: ', chosen_anime)
print(get_recommendation(chosen_anime))


end = time.time()
print("Full run of code: ", '{:0.2f}'.format(time.time()-start))
