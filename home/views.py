from django.shortcuts import render


def landing_page(request):
    return render(request, 'home/landing_page.html')


def main(request):
    return render(request, 'home/main.html')

def gunbti(request):
    return render(request, 'home/gunbti.html')

def results(request, count):
    
    return render(request, 'home/results.html')