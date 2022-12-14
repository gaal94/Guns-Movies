from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('main/', views.main, name='main'),
    path('gunbti/', views.gunbti, name='gunbti'),
    path('results/<int:count>', views.results, name='results'),
]
