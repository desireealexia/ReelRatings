from django.urls import path
from .views import HomePageView, MovieDetailView, SearchResultsView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('movie/<int:movie_id>/', MovieDetailView.as_view(), name='movie_detail'),
    path('search/', SearchResultsView.as_view(), name='search_results'),

]