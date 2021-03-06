# Generated by Django 3.1.2 on 2020-10-11 00:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='mal_anime_prod',
            fields=[
                ('anime_id', models.IntegerField(primary_key=True, serialize=False)),
                ('title_japanese', models.CharField(max_length=200)),
                ('title_english', models.CharField(max_length=200, null=True)),
                ('image_url', models.URLField(null=True)),
                ('anime_type', models.CharField(max_length=200, null=True)),
                ('genres', models.JSONField(null=True)),
                ('episodes', models.IntegerField(null=True)),
                ('mal_url', models.URLField(null=True)),
                ('synopsis', models.CharField(max_length=200, null=True)),
                ('trailer_url', models.URLField(null=True)),
                ('rating', models.DecimalField(decimal_places=2, max_digits=4, null=True)),
                ('members', models.IntegerField(null=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='mal_user_prod',
            fields=[
                ('user_id', models.IntegerField(primary_key=True, serialize=False)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='mal_rating_prod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(null=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('anime_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recommender.mal_anime_prod')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recommender.mal_user_prod')),
            ],
        ),
    ]
