# Generated by Django 3.1.2 on 2020-12-31 12:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0005_auto_20201010_2112'),
    ]

    operations = [
        migrations.CreateModel(
            name='MergedRatings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anime', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recommender.mal_anime_prod')),
                ('rating', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recommender.mal_rating_prod')),
            ],
        ),
    ]
