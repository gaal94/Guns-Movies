from django.shortcuts import get_object_or_404, render, get_list_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_safe, require_POST, require_http_methods
from .models import Movie, Genre
from django.http import JsonResponse
from .forms import MovieForm
import requests


@require_safe
def index(request):
    if request.GET.get('search_keyword'):
        search_keyword = request.GET.get('search_keyword')
        if request.GET.get('search_type') == 'search_by_title':
            movies = Movie.objects.filter(title__icontains=search_keyword)
        elif request.GET.get('search_type') == 'search_by_genre':
            movies = Movie.objects.filter(genres__name__icontains=search_keyword)
    else:
        movies = get_list_or_404(Movie)
    context = {
        'movies': movies,
    }
    return render(request, 'movies/index.html', context)


@require_http_methods(['GET', 'POST'])
def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == 'POST':
        if request.user.is_superuser:
            movie.delete()
            return redirect('movies:index')
        else:
            print('not superuser')
    else:
        context = {
            'movie': movie,
        }
        return render(request, 'movies/detail.html', context)


@require_POST
def like(request, movie_pk):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, pk=movie_pk)
        user = request.user

        if movie.like_users.filter(pk=user.pk).exists():
            movie.like_users.remove(user)
            liked = False
        else:
            movie.like_users.add(user)
            liked = True
        count = movie.like_users.count()
        context = {
            'liked': liked,
            'count': count,
        }
        return JsonResponse(context)
    return redirect('accounts:login')


@login_required
@require_http_methods(['GET', 'POST'])
def db(request):
    if request.method == 'POST':
        if request.user.is_superuser:
            form = MovieForm()
            movie = form.save(commit=False)
            movie.title = request.POST.get('title')
            movie.release_date = request.POST.get('release_date')
            movie.popularity = request.POST.get('popularity')
            movie.vote_count = request.POST.get('vote_count')
            movie.vote_average = request.POST.get('vote_average')
            movie.overview = request.POST.get('overview')
            movie.poster_path = request.POST.get('poster_path')
            movie.save()
            genre_ids = request.POST.get('genre_ids')
            for genre_id in genre_ids[1:-1].split(', '):
                genre = get_object_or_404(Genre, pk=genre_id)
                movie.genres.add(genre)
            return redirect('movies:update', movie.title)
        else:
            print('not superuser')
    else:
        if request.user.is_superuser:
            if request.GET.get('search_keyword'):
                search_keyword = request.GET.get('search_keyword')
                movies = Movie.objects.all()
                movie_titles = []
                for movie in movies:
                    movie_titles.append(movie.title)
                BASE_URL = 'https://api.themoviedb.org/3'
                path = '/search/movie'
                params = {
                    'api_key': '05752707a030a1c74935741bb5d3e4e3',
                    'region': 'KR',
                    'language': 'ko',
                    'query': search_keyword,
                }
                response = requests.get(BASE_URL+path, params=params)
                data = response.json()
                context = {
                    'data': data,
                    'movie_titles': movie_titles,
                }
                return render(request, 'movies/db.html', context)
            else:
                return render(request, 'movies/db.html')
        else:
            print('not superuser')


@login_required
@require_http_methods(['GET', 'POST'])
def update(request, movie_title):
    movie = get_object_or_404(Movie, title=movie_title)
    if request.method == 'POST':
        if request.user.is_superuser:
            form = MovieForm(request.POST, instance=movie)
            if form.is_valid():
                form.save()
                return redirect('movies:detail', movie.pk)
            context = {
                'form': form,
            }
            return render(request, 'movies/update.html', context)
        else:
            print('not superuser')
    else:
        if request.user.is_superuser:
            form = MovieForm(instance=movie)
            context = {
                'form': form,
            }
            return render(request, 'movies/update.html', context)
        else:
            print('not superuser')