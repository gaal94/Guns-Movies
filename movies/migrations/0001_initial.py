# Generated by Django 3.2.12 on 2022-05-20 06:55

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('guns', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('release_date', models.DateField()),
                ('popularity', models.FloatField()),
                ('vote_count', models.IntegerField()),
                ('vote_average', models.FloatField()),
                ('overview', models.TextField()),
                ('poster_path', models.CharField(max_length=200)),
                ('genres', models.ManyToManyField(to='movies.Genre')),
                ('like_users', models.ManyToManyField(blank=True, related_name='like_movies', to=settings.AUTH_USER_MODEL)),
                ('related_guns', models.ManyToManyField(blank=True, related_name='related_movies', to='guns.Gun')),
            ],
        ),
    ]