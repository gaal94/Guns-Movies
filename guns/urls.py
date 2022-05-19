from django.urls import path
from . import views

app_name = 'guns'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:gun_pk>/', views.detail, name='detail'),
    path('<int:gun_pk>/like/', views.like, name='like'),
]