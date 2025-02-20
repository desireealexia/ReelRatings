from django.shortcuts import render
from django.views import View
from .utils import get_tmdb_data

# Create your views here.
class HomePageView(View):
    def get(self, request):
        popular_movies = get_tmdb_data('movie/popular', {
            'language': 'en-US', 
            'page': 1
        })
        return render(request, 'movies/home.html', {'movies': popular_movies['results']})

class MovieDetailView(View):
    def get(self, request, movie_id):
        movie = get_tmdb_data(f"movie/{movie_id}", {
            'language': 'en-US'
        })
        recommendations = get_tmdb_data(f"movie/{movie_id}/recommendations", {'language': 'en-US'})
        return render(request, 'movies/detail.html', {
            'movie': movie,
            'recommendations': recommendations['results']
        })
        
class SearchResultsView(View):
    def get(self,request):
        query = request.GET.get('q', '')
        search_results = []
        
        if query:
            search_results = get_tmdb_data('search/movie', {
                'query': query, 'language': 'en-US'})['results']
        
        return render(request, 'movies/search_results.html', {
            'movies': search_results,
            'query': query
        })