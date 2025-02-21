from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.conf import settings
import requests
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
        
        recommendations_list = recommendations.get('results', [])
        return render(request, 'movies/movie_detail.html', {
            'movie': movie,
            'recommendations': recommendations_list
        })
        
class TVShowDetailView(View):
    def get(self, request, series_id):
        show = get_tmdb_data(f"tv/{series_id}", {
            'language': 'en-US'
        })
        recommendations = get_tmdb_data(f"tv/{series_id}/recommendations", {'language': 'en-US'})
        
        recommendations_list = recommendations.get('results', [])
        return render(request, 'movies/tv_show_detail.html', {
            'show': show,
            'recommendations': recommendations_list
        })
        
class SearchResultsView(View):
    def get(self, request):
        query = request.GET.get('q', '')  # Get search query
        search_results = get_tmdb_data(f"search/multi?query={query}")

        context = {
            "query": query,
            "results": search_results.get('results', []),}

        return render(request, "movies/search_results.html", context)