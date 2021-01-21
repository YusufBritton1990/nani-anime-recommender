from recommender.scripts import postgres_credentials as pg
import time
import numpy as np
import pandas as pd

"""Recommendation functions"""
def check_genre(genre_list,string):
    if any(x in string for x in genre_list):
        return True
    else:
        return False

def get_recommendation(chosen_anime_id):
    start = time.time()

    """Assigning Dataframes"""
    print('Gathering Recommendations: ', chosen_anime_id)

    print('Querying Animes')
    anime_df = pd.read_sql_query(pg.anime_query(),pg.pg_connection())
    print('Completed in: ', '{:0.2f}'.format(time.time()-start))

    param = {'chosen_anime_id' : chosen_anime_id}

    print('Querying subset for: ', chosen_anime_id)
    user_subset_df = pd.read_sql_query(pg.merge_subset_query(),
                        pg.pg_connection(), params=param)
    print('Completed in: ', '{:0.2f}'.format(time.time()-start))

    """Creating relationship tables"""
    # Construct average scores of animes
    rating_mean_df = pd.DataFrame(user_subset_df.groupby('anime_id_id')['rating'].mean())
    rating_mean_df['num of ratings'] = pd.DataFrame(user_subset_df.groupby('anime_id_id')['rating'].count())

    # Pick the genres from this selection
    genre_dict = pd.DataFrame(data=anime_df[['anime_id','genres']])
    genre_dict.set_index('anime_id',inplace=True) #This is what is ingested


    #generating list of anime with the same genre with target
    anime_genre = genre_dict.loc[chosen_anime_id].values[0].split(', ')
    cols = anime_df[anime_df['genres'].apply(
        lambda x: check_genre(anime_genre,str(x)))]['anime_id'].tolist()

    #create matrix based on generated list
    animemat = user_subset_df[user_subset_df['anime_id_id'].isin(cols)].pivot_table(
        index='user_id_id',columns='anime_id_id',values='rating')

    #create correlation table
    anime_user_rating = animemat[chosen_anime_id]
    similiar_anime = animemat.corrwith(anime_user_rating)
    corr_anime = pd.DataFrame(similiar_anime,columns=['correlation'])
    corr_anime = corr_anime.join(rating_mean_df['num of ratings'])
    corr_anime.dropna(inplace=True)

    rating_quantile = int(round(corr_anime['num of ratings'].quantile(.25), 0))
    corr_anime = corr_anime[corr_anime['num of ratings'] > rating_quantile].sort_values(
        'correlation',ascending=False)

    corr_anime['title_japanese'] = corr_anime.index.map(
    anime_df.set_index('anime_id')['title_japanese'].to_dict()
    )

    end = time.time()
    print("Full run of code: ", '{:0.2f}'.format(time.time()-start))

    return corr_anime.head(10)

# Test
# chosen_anime = 'Hajime no Ippo'
# chosen_anime = 'Naruto'
# chosen_anime = 20
# chosen_anime = 263
#
# print(get_recommendation(chosen_anime))
