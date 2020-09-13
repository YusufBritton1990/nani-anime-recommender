from django.shortcuts import render
from django.http import Http404
# from django.template import loader

def index(request):
    # TODO: Include context to dynamically load pages
    # TODO: Include 404 if page doesn't exist
    # https://docs.djangoproject.com/en/3.1/intro/tutorial03/
    # try:

    return render(request, 'recommender/anime-detail.html')

    # except
