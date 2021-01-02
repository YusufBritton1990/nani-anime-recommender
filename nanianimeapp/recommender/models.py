from django.db import models

# Create your models here.
class mal_anime_prod(models.Model):
    """Detail of animes"""
    anime_id = models.IntegerField(primary_key=True)
    title_japanese = models.CharField(max_length=200)
    title_english = models.CharField(null=True, max_length=200)
    image_url = models.URLField(null=True)
    anime_type = models.CharField(null=True, max_length=200)
    genres = models.CharField(null=True, max_length=200)
    episodes = models.IntegerField(null=True)
    mal_url = models.URLField(null=True)
    synopsis = models.CharField(null=True, max_length=50000)
    trailer_url = models.URLField(null=True)
    rating = models.DecimalField(null=True,max_digits=4,decimal_places=2)
    members = models.IntegerField(null=True)
    update_time = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title_japanese #returns japanese name when object queried


class mal_user_prod(models.Model):
    """MAL user IDs"""
    user_id = models.IntegerField(primary_key=True)
    update_time = models.DateTimeField(auto_now=True)

class mal_rating_prod(models.Model):
    """Ratings of animes from MAL users"""
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(mal_user_prod, on_delete=models.CASCADE)
    anime_id = models.ForeignKey(mal_anime_prod, on_delete=models.CASCADE)
    rating = models.IntegerField(null=True)
    update_time = models.DateTimeField(auto_now=True)

class mal_merged_ratings_prod(models.Model):
    """
    Rating table used in algorithm.
    Only contains animes ratings with at least 10K reviews.
    combination of mal_rating_prod and mal_anime_prod
    """
    id = models.AutoField(primary_key=True)
    anime_id = models.ForeignKey(mal_anime_prod, on_delete=models.CASCADE)
    user_id = models.ForeignKey(mal_user_prod, on_delete=models.CASCADE)
    title_japanese = models.CharField(max_length=200)
    rating = models.IntegerField(null=True)
