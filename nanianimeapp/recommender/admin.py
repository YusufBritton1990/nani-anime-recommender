from django.contrib import admin
from .models import mal_anime_prod, mal_rating_prod, mal_user_prod
# Register your models here.

class AnimeAdmin(admin.ModelAdmin):
    list_display = ("anime_id", "title_japanese","title_english",)

class RatingAdmin(admin.ModelAdmin):
    list_display = ("user_id", "anime_id","rating",)

class UserAdmin(admin.ModelAdmin):
    list_display = ("user_id", )


admin.site.register(mal_anime_prod, AnimeAdmin)
admin.site.register(mal_rating_prod, RatingAdmin)
admin.site.register(mal_user_prod, UserAdmin)
