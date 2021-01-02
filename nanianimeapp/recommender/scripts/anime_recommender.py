import postgres_credentials as pg
import time
import numpy as np
import pandas as pd

"""Recommendation functions"""
def check_genre(genre_list,string):
    if any(x in string for x in genre_list):
        return True
    else:
        return False

# TODO: When looking a anime with a small poll of viewing, dynamically update ['num of ratings']
def get_recommendation(chosen_anime):
    start = time.time()

    """Assigning Dataframes"""

    print('Querying Animes')
    anime_df = pd.read_sql_query(pg.anime_query(),pg.pg_connection())
    print('Completed in: ', '{:0.2f}'.format(time.time()-start))

    param = {'anime' : chosen_anime}

    print('Querying subset for: ', chosen_anime)
    user_subset_df = pd.read_sql_query(pg.merge_subset_query(),
                        pg.pg_connection(), params=param)
    print('Completed in: ', '{:0.2f}'.format(time.time()-start))

    """Creating relationship tables"""
    # Construct average scores of animes
    rating_mean_df = pd.DataFrame(user_subset_df.groupby('title_japanese')['rating'].mean())
    rating_mean_df['num of ratings'] = pd.DataFrame(user_subset_df.groupby('title_japanese')['rating'].count())

    # Pick the genres from this selection
    genre_dict = pd.DataFrame(data=anime_df[['title_japanese','genres']])
    genre_dict.set_index('title_japanese',inplace=True) #This is what is ingested


    #generating list of anime with the same genre with target
    anime_genre = genre_dict.loc[chosen_anime].values[0].split(', ')
    cols = anime_df[anime_df['genres'].apply(
        lambda x: check_genre(anime_genre,str(x)))]['title_japanese'].tolist()

    #create matrix based on generated list
    animemat = user_subset_df[user_subset_df['title_japanese'].isin(cols)].pivot_table(
        index='user_id_id',columns='title_japanese',values='rating')

    #create correlation table
    anime_user_rating = animemat[chosen_anime]
    similiar_anime = animemat.corrwith(anime_user_rating)
    corr_anime = pd.DataFrame(similiar_anime,columns=['correlation'])
    corr_anime = corr_anime.join(rating_mean_df['num of ratings'])
    corr_anime.dropna(inplace=True)

    rating_quantile = int(round(corr_anime['num of ratings'].quantile(.25), 0))
    corr_anime = corr_anime[corr_anime['num of ratings'] > 100].sort_values(
        'correlation',ascending=False)

    end = time.time()
    print("Full run of code: ", '{:0.2f}'.format(time.time()-start))

    return corr_anime.head(10)

# Test
# chosen_anime = 'Hajime no Ippo'
chosen_anime = 'Naruto'

print('Gathering Recommendations: ', chosen_anime)
print(get_recommendation(chosen_anime))
