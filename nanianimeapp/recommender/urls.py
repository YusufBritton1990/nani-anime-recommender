from django.urls import path, re_path

from . import views

# autocomplete not working. look at recommender.views for notes
urlpatterns = [
    path('', views.anime_search, name='search'),
    path('listing', views.anime_listing, name='listing'),
    # path('listing', views.anime_listing.as_view(), name='listing'),
    path('results', views.anime_results.as_view(), name='results'),
    path('<int:anime_id>/detail', views.anime_detail, name='detail'),
    # path('results', views.anime_results, name='results'),

    # re_path( r'^anime-autocomplete/$', views.AnimeAutocomplete.as_view(),
    #     name='anime-autocomplete',),
]
