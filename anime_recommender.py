from postgres_credentials import anime_query, ratings_query, merge_subset_query, merge_query

import time

# Look into this later
# from sklearn.preprocessing import StandardScaler
# from sklearn.decomposition import PCA
# from sklearn.cluster import KMeans
# from sklearn.metrics import silhouette_score


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
# %matplotlib inline #Used in jupyter notebook


start = time.time()

# Assigning Dataframes
# TODO: Replace with database connection
# rating_df = pd.read_csv('../data/rating.csv')
# anime_df = pd.read_csv('../data/anime.csv')

rating_df = pd.DataFrame(ratings_query(), columns=['user_id','anime_id','rating

anime_df = pd.DataFrame(anime_query(), columns=['anime_id','name','genre', 'type', 'episodes', 'rating', 'members'])

print("Printing ratings_df")
print(rating_df.head())

# # Merge Dataframes and subset
# # TODO: Running into a memory problem. For now, saving DF
# merged_df = pd.merge(rating_df,anime_df.drop('rating',axis=1),on='anime_id')
# # merged_df.to_csv('../data/merged_df.csv')
#
# #Temporary solution for memory problem
# # merged_df = pd.read_csv('../data/merged_df.csv')
#
# merged_10k_df = merged_df[merged_df["members"] > 10000]
# merged_10k_df = merged_10k_df[merged_10k_df["rating"] > -1]
#
# user_watched_df = merged_10k_df[['user_id', 'name']]# dataframe of users that watched animes
# user_watched_df = user_watched_df.loc[user_watched_df['name'] == anime]
#
# # List of users who watched the chosen anime
# unique_users_array = user_watched_df.user_id.unique()
#
# # Subset data to only include users that watched the chosen anime, including all other animes watched
# user_subset_df = merged_10k_df[merged_10k_df.user_id.isin(unique_users_array)]
#
# # Subset anime_df based on unique users
# # anime_df = anime_df[anime_df.user_id.isin(unique_users_array)]
#
# # Construct average scores of animes
# rating_mean_df = pd.DataFrame(user_subset_df.groupby('name')['rating'].mean())
# rating_mean_df['num of ratings'] = pd.DataFrame(user_subset_df.groupby('name')['rating'].count())
#
# # Pic the genres from this selection
# # TODO: See if you have to subset anime_df also
# genre_dict = pd.DataFrame(data=anime_df[['name','genre']])
# genre_dict.set_index('name',inplace=True) #This is what is ingested
#
#
# def check_genre(genre_list,string):
#     if any(x in string for x in genre_list):
#         return True
#     else:
#         return False
#
# def get_recommendation(name):
#     #generating list of anime with the same genre with target
#     anime_genre = genre_dict.loc[name].values[0].split(', ') #
#     cols = anime_df[anime_df['genre'].apply(
#         lambda x: check_genre(anime_genre,str(x)))]['name'].tolist()
#
#     #create matrix based on generated list
#     animemat = user_subset_df[user_subset_df['name'].isin(cols)].pivot_table(
#         index='user_id',columns='name',values='rating')
#
#     #create correlation table
#     anime_user_rating = animemat[name]
#     similiar_anime = animemat.corrwith(anime_user_rating)
#     corr_anime = pd.DataFrame(similiar_anime,columns=['correlation'])
#     corr_anime = corr_anime.join(rating_mean_df['num of ratings'])
#     corr_anime.dropna(inplace=True)
#     corr_anime = corr_anime[corr_anime['num of ratings'] > 1000].sort_values(
#         'correlation',ascending=False)
#
#     return corr_anime.head(10)
#
# # Test
# get_recommendation('Mushishi')
#
# end = time.time()
# print(end - start)
