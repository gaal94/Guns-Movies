from django.shortcuts import render


def landing_page(request):
    return render(request, 'landing_page.html')


def main(request):
    return render(request, 'main.html')