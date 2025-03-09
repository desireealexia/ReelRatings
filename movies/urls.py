from django.urls import path
from . import views

urlpatterns = [
    # Home Page
    path('', views.HomePageView.as_view(), name='home'),
    path('movie/<int:movie_id>/', views.MovieDetailView.as_view(), name='movie_detail'),
    path('tv_show/<int:series_id>/', views.TVShowDetailView.as_view(), name='tv_show_detail'),
    path('search/', views.SearchResultsView.as_view(), name='search_results'),
]