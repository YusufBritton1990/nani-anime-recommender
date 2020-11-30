from django.urls import path

from . import views

urlpatterns = [
    path('', views.anime_recommender, name='recommender'),
    path('<int:anime_id>/detail', views.anime_detail, name='detail'),
    # path('results', views.anime_results, name='results'),
    path('results', views.anime_results.as_view(), name='results'),
]
