from django.urls import path
from .views import HomePageView, SearchResultsView, MovieDetailView, TVShowDetailView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('movie/<int:movie_id>/', MovieDetailView.as_view(), name='movie_detail'),
    path('tv-show/<int:series_id>/', TVShowDetailView.as_view(), name='tv_show_detail'),
]