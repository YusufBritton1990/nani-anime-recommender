from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.http import Http404
from django.db.models import Q

from .models import mal_anime_prod

from .scripts.mal_jikan_anime import get_anime

import datetime

def anime_recommender(request):
    return render(request, 'recommender/index.html')

class anime_results(ListView):
    model = mal_anime_prod
    template_name = 'recommender/anime-results.html'

    def get_queryset(self): # new
        query = self.request.GET.get('q')
        # print(query)
        object_list  = mal_anime_prod.objects.filter(
                Q(title_japanese__icontains=query) |
                 Q(title_english__icontains=query)
            )

        return object_list

# def anime_results(request):
    # Store the id from the recommender like this
    # anime_id_list = [1,2,3,4,5]

    # sampling what it will look like
    # anime1 = mal_anime_prod.objects.get(anime_id=1)
    # anime2 = mal_anime_prod.objects.get(anime_id=5)

    # anime_id_list = {anime1, anime2}
    #
    # return render(request, 'recommender/anime-results.html', {'anime_id_list' : anime_id_list})

def anime_detail(request, anime_id):
    # Call to most recent anime data
    data = get_anime(anime_id,anime_id)

    # update anime database will called values
    today = datetime.date.today()

    if data[12].day <  today.day:
        print(f'updating anime id {anime_id} at {data[12]}')

        # NOTE: trailer_url is omiting query parameters
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
