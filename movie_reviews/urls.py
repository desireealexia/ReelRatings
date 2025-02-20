from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('movies/', views.movie_list, name='movie_list'),
    path('movies/<slug:slug>/', views.movie_detail, name='movie_detail'),
    path('search/', views.search, name='search'),
    path('tv-shows/', views.tv_show_list, name='tv_show_list'),
    path('tv-shows/<slug:slug>/', views.tv_detail, name='tv_detail'),
]