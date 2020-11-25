from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:anime_id>/detail', views.anime_detail, name='detail'),
    path('results', views.anime_results, name='results')
]
