from django.shortcuts import get_object_or_404, render, get_list_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_safe, require_POST
from .models import Movie
from random import sample
from datetime import datetime
from datetime import timedelta
from django.http import JsonResponse
# Create your views here.
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
        'movies': movies
    }
    return render(request, 'movies/index.html', context)


@require_safe
def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    context = {
        'movie':movie
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