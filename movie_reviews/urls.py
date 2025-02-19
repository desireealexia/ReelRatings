from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('movies/<slug:slug>/', views.movie_detail, name='movie_detail'),
    path('search/', views.search, name='search'),
    path('tv/<slug:slug>/', views.tv_detail, name='tv_detail'),
]