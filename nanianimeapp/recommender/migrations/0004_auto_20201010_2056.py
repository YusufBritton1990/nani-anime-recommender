# Generated by Django 3.1.2 on 2020-10-11 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0003_auto_20201010_2051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mal_anime_prod',
            name='synopsis',
            field=models.CharField(max_length=50000, null=True),
        ),
    ]
