from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('movies/<slug:slug>/', views.movie_detail, name='movie_detail'),
    path('search/', views.search_movies, name='search_movies'),
]