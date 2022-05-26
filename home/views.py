from django.shortcuts import render, get_list_or_404
from movies.models import Movie
from guns.models import Gun


def landing_page(request):
    return render(request, 'home/landing_page.html')


def main(request):
    return render(request, 'home/main.html')

def gunbti(request):
    return render(request, 'home/gunbti.html')

def results(request, count):
    if count >= 12:
        your_gun = 'Machine Gun'
    elif count >= 10:
        your_gun = 'Assault Rifle'
    elif count >= 8:
        your_gun = 'Submachine Gun'
    elif count >= 4:
        your_gun = 'Pistol'
    elif count >= 2:
        your_gun = 'Shotgun'
    elif count >= 0:
        your_gun = 'Sniper Rifle'
    
    guns = Gun.objects.filter(gun_type__type_name__exact=your_gun)
    #  movies = Movie.objects.filter(related_guns__gun_name__icontains = guns)
    movies = Movie.objects.filter(related_guns__gun_type__type_name__exact=your_gun)
    movie = movies.order_by('?')[0]
    
    
    

    context = {
        'your_gun' : your_gun,
        'count' : count,
        'movies' : movies,
        'movie' : movie,
        'guns' : guns,
    }
    
    return render(request, 'home/results.html', context)