# django packages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, ListView
from django.http import Http404, JsonResponse
from django.db.models import Q #needed for complex queries
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# models
from recommender.models import mal_anime_prod

# scripts
# from recommender.scripts.mal_jikan_anime import get_anime
from recommender.scripts.mal_api_anime import get_anime
from recommender.scripts.anime_recommender import get_recommendation
# from dal import autocomplete #update settings too

# Misc
import datetime
import pytz #allows using tz classes to make UTC time usuable
import os
import requests


def anime_search(request):
    return render(request, 'recommender/index.html')

def mal_auth(request):
    """
    From Step 2: Client requests OAuth 2.0 authentication
    https://myanimelist.net/apiconfig/references/authorization#step-1-generate-a-code-verifier-and-challenge
    """

    base_url = f'https://myanimelist.net/v1/oauth2/authorize?'
    response_type = 'code'
    client_id = os.environ['MAL_CLIENT_ID']
    state = 'authid100'
    code_challenge = os.environ['MAL_CODE_CHALLENGE']
    # code_challenge_method = 'plain' #optional, defaults to plain

    #optional, redirect to search page
    # redirect_uri = 'http://localhost:8000/'

    auth_url = f'{base_url}response_type={response_type}'
    auth_url = f'{auth_url}&client_id={client_id}&code_challenge={code_challenge}'
    # auth_url = f'{auth_url}&state={state}&redirect_uri={redirect_uri}'
    auth_url = f'{auth_url}&state={state}'

    return HttpResponseRedirect(auth_url)

def mal_auth_response(request):
    """
    From Step 5: MyAnimeList redirects back to the client
    and
    Step 6: Exchange authorization code for refresh and access tokens
    https://myanimelist.net/apiconfig/references/authorization#step-1-generate-a-code-verifier-and-challenge
    """
    base_url = 'https://myanimelist.net/v1/oauth2/token'

    client_id = os.environ['MAL_CLIENT_ID']
    client_secret = os.environ['MAL_CLIENT_SECRET']
    code = request.GET.get('code') #populates when user is authenticated

    data = {
        'client_id' : client_id,
        'client_secret' : client_secret,
        'grant_type' : 'authorization_code',
        'code' : code,
        'code_verifier': os.environ['MAL_CODE_VERIFIER']
    }

    # External call for token data, using requests library
    response = requests.post(base_url, data=data)
    response_dict = response.json()

    # TODO: This information needs to be stored once user is authenticated.
    # Need to add this into the user app once created
    # print(f"Token Type: {response_dict['token_type']}")
    # print(f"Expires in:  {response_dict['expires_in']}")
    # print(f"Access Token: {response_dict['access_token']}")
    # print(f"Refresh Token: {response_dict['refresh_token']}")

    # TODO: Temporary, need to store this in a database when user app created
    # which will be used for each user

    # Saving data within a session
    request.session['access_token']  = response_dict['access_token']

    return redirect('search')

def anime_listing(request):
    """List animes to select from that contains searched term (q)"""
    anime_list  = mal_anime_prod.objects.all()
    query = request.GET.get('q')

    if query:
        anime_list  = mal_anime_prod.objects.exclude(members__isnull=True).filter(
                Q(title_japanese__icontains=query) |
                 Q(title_english__icontains=query)
            ).order_by('-members')

    paginator = Paginator(anime_list, 9)
    page = request.GET.get('page')

    try:
        anime_list = paginator.page(page)
    except PageNotAnInteger:
        anime_list = paginator.page(1)
    except EmptyPage:
        anime_list = paginator.page(paginator.num_pages)

    context = {'animes' : anime_list}

    return render(request, 'recommender/anime-listing.html', context)

# TODO: Fix NoReverse match error
def anime_processing(request):
    chosen_anime_id = 20 # Naruto
    recommend_df = get_recommendation(chosen_anime_id)
    anime_list = recommend_df.index.format()
    anime_str = ','.join(anime_list)

    redirect('results', q = anime_str)

class anime_results(ListView):
    model = mal_anime_prod
    template_name = 'recommender/anime-results.html'

    def get_queryset(self): # new
        query = self.request.GET.get('q')
        # print(query)
        object_list  = mal_anime_prod.objects.filter(anime_id__in=query)

        return object_list


def anime_detail(request, anime_id):
    # Check if database is updated for today
    today = datetime.date.today().strftime('%Y-%m-%d')

    db_anime_time = mal_anime_prod.objects.get(pk=anime_id).update_time
    db_anime_date = db_anime_time.strftime('%Y-%m-%d')

    # if the query date isnt the same day, update anime detail
    if db_anime_date != today:
        print(f'\nupdating anime id {anime_id} at {db_anime_time}\n')

        # Call to most recent anime data
        access_token = request.session['access_token'] #needed to use MAL api
        # anime_dict = get_anime(anime_id,anime_id, access_token)
        anime_json = get_anime(anime_id,anime_id, access_token)[0]

        # NOTE: trailer_url is omiting query parameters
        # TODO: Need to be able to update trailer_url
        # update_anime_detail = mal_anime_prod.objects.filter(pk=anime_id).update(
        # title_japanese = anime_dict['title_japanese'],
        # title_english = anime_dict['title_english'],
        # image_url = anime_dict['image_url'],
        # anime_type = anime_dict['anime_type'],
        # genres = anime_dict['genres'], episodes = anime_dict['episodes'],
        # mal_url = anime_dict['mal_url'], synopsis = anime_dict['synopsis'],
        # rating = anime_dict['rating'],
        # # trailer_url = data[9].split('?')[0], rating = data[10],
        # members = anime_dict['members'], update_time = anime_dict['update_time']
        # )

        # try statements
        try:
            title_english = anime_json['alternative_titles']['en']
        # print("Name of anime (English): ",anime_json['alternative_titles']['en'])

        except TypeError:
            title_english = None

        # genres
        genre_list = []
        for genre in anime_json['genres']:
            genre_list.append(genre['name'])
            # print("Genre: ", genre['name'])
        genre_list = ', '.join(genre_list)

        # urls
        base_url = "https://myanimelist.net/anime"
        mal_title = anime_json['title'].replace(" ", "_")
        mal_url = f"{base_url}/{anime_json['id']}/{mal_title}"

        # update_time
        update_time = datetime.datetime.now(pytz.utc)

        # updating anime with new infomation
        update_anime_detail = mal_anime_prod.objects.filter(pk=anime_id).update(
        title_japanese = anime_json['title'],
        title_english = title_english,
        image_url = anime_json['main_picture']['medium'],
        anime_type = anime_json['media_type'],
        genres = genre_list, episodes = anime_json['num_episodes'],
        mal_url = mal_url, synopsis = anime_json['synopsis'],
        rating = anime_json['mean'],
        # trailer_url = data[9].split('?')[0], rating = data[10],
        members = anime_json['num_scoring_users'], update_time = update_time
        )

    # Rendering
    chosen_anime = get_object_or_404(mal_anime_prod, pk=anime_id)
    return render(request, 'recommender/anime-detail.html', {'chosen_anime' : chosen_anime})


# Pending
    # TODO: Javascript autocomplete not connecting to models as a string. Test using
    # Djando autocomplete classes
    # ref: https://django-autocomplete-light.readthedocs.io/en/master/tutorial.html

    # class AnimeAutocomplete(autocomplete.Select2QuerySetView):
    #     def get_queryset(self):
    #         # Don't forget to filter out results depending on the visitor !
    #         # if not self.request.user.is_authenticated:
    #         #     return mal_anime_prod.objects.none()
    #
    #         qs = mal_anime_prod.objects.all()
    #
    #         if self.q:
    #             qs = qs.exclude(members__isnull=True).filter(
    #                     Q(title_japanese__icontains=self.q) |
    #                      Q(title_english__icontains=self.q)
    #                 ).order_by('-members')[:10]
    #
    #         return qs
