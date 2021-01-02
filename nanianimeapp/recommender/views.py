# django packages
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.http import Http404, JsonResponse
from django.db.models import Q #needed for complex queries
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# models
from recommender.models import mal_anime_prod

# scripts
from recommender.scripts.mal_jikan_anime import get_anime
# from dal import autocomplete #update settings too

# Misc
import datetime

def anime_search(request):
    return render(request, 'recommender/index.html')


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


class anime_results(ListView):
    model = mal_anime_prod
    template_name = 'recommender/anime-results.html'

    def get_queryset(self): # new
        query = self.request.GET.get('q')
        # print(query)
        object_list  = mal_anime_prod.objects.exclude(members__isnull=True).filter(
                Q(title_japanese__icontains=query) |
                 Q(title_english__icontains=query)
            ).order_by('-members')[:5]

        return object_list


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
