from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View
from .utils import get_tmdb_data

# Create your views here.
class HomePageView(View):
    def get(self, request):
        # Fetch popular movies and TV shows from TMDb API
        popular_movies = get_tmdb_data('movie/popular', {
            'language': 'en-US', 
            'page': request.GET.get('movie_page', 1)
        })
                
        popular_tv_shows = get_tmdb_data('tv/popular', {
            'language': 'en-US',
            'page': request.GET.get('tv_show_page', 1)
        })
        
          # Pagination for movies and TV shows
        movie_page_number = request.GET.get('movie_page', 1)
        tv_show_page_number = request.GET.get('tv_show_page', 1)

        movie_paginator = Paginator(popular_movies.get('results', []), 4)  # Show 12 results per page
        tv_show_paginator = Paginator(popular_tv_shows.get('results', []), 4)  # Show 12 results per page

        movie_page_obj = movie_paginator.get_page(movie_page_number)
        tv_show_page_obj = tv_show_paginator.get_page(tv_show_page_number)

        context = {
            'movie_page_obj': movie_page_obj,
            'tv_show_page_obj': tv_show_page_obj
        }
         
        return render(request, 'movies/home.html', context)

class MovieDetailView(View):
    def get(self, request, movie_id):
        movie = get_tmdb_data(f"movie/{movie_id}", {
            'language': 'en-US'
        })
        recommendations = get_tmdb_data(f"movie/{movie_id}/recommendations", {'language': 'en-US'})
        return render(request, 'movies/movie_detail.html', {
            'movie': movie,
            'recommendations': recommendations['results']
        })
        
class TVShowDetailView(View):
    def get(self, request, show_id):
        show = get_tmdb_data(f"tv/{show_id}", {
            'language': 'en-US'
        })
        recommendations = get_tmdb_data(f"tv/{show_id}/recommendations", {'language': 'en-US'})
        return render(request, 'movies/tv_show_detail.html', {
            'show': show,
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