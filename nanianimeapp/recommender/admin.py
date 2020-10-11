from django.contrib import admin
from .models import mal_anime_prod, mal_rating_prod, mal_user_prod
# Register your models here.
admin.site.register(mal_anime_prod)
admin.site.register(mal_rating_prod)
admin.site.register(mal_user_prod)
