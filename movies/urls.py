from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:movie_pk>/', views.detail, name='detail'),
    path('<int:movie_pk>/like/', views.like, name='like'),
    path('db/', views.db, name='db'),
    path('gundb/', views.gundb, name='gundb'),
    path('<movie_title>/update', views.update, name='update'),
]
