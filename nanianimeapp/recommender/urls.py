from django.urls import path, re_path

from . import views

# autocomplete not working. look at recommender.views for notes
urlpatterns = [
    path('', views.anime_search, name='search'),
    path('auth', views.mal_auth, name='auth'),
    path('auth-reponse', views.mal_auth_response, name='auth-reponse'),
    path('listing', views.anime_listing, name='listing'),
    path('processing', views.anime_processing, name='processing'),
    path('results', views.anime_results.as_view(), name='results'),
    path('<int:anime_id>/detail', views.anime_detail, name='detail'),

    # re_path( r'^anime-autocomplete/$', views.AnimeAutocomplete.as_view(),
    #     name='anime-autocomplete',),
]
