from django.shortcuts import render, get_object_or_404
from django.http import Http404
# from django.template import loader
from .models import mal_anime_prod

from .scripts.mal_jikan_anime import get_anime

import datetime

def index(request):
    # TODO: Include context to dynamically load pages
    # TODO: Include 404 if page doesn't exist
    # https://docs.djangoproject.com/en/3.1/intro/tutorial03/
    # try:

    return render(request, 'recommender/anime-detail-draft.html')

    # except

def anime_detail(request, anime_id):
    # Call to most recent anime data
    data = get_anime(anime_id,anime_id)

    # update anime database will called values
    today = datetime.date.today()

    if data[12].day <  today.day:
        print(f'updating anime id {anime_id} at {data[12]}')

        update_anime_detail = mal_anime_prod.objects.filter(pk=anime_id).update(
        title_japanese = data[1], title_english = data[2],
        image_url = data[3], anime_type = data[4],
        genres = data[5], episodes = data[6],
        mal_url = data[7], synopsis = data[8],
        trailer_url = data[9].split('?')[0], rating = data[10],
        members = data[11], update_time = data[12]
        )

    # Rendering
    chosen_anime = get_object_or_404(mal_anime_prod, pk=anime_id)
    return render(request, 'recommender/anime-detail.html', {'chosen_anime' : chosen_anime})
