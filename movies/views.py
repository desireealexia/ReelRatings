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
        genre_filter = request.GET.get('genre', '')  # Get genre filter
        sort_by = request.GET.get('sort', 'popularity.desc')  # Default sort by popularity

        params = {
            'query': query,
            'language': 'en-US',
            'page': 1,
        }

        search_results = get_tmdb_data('search/multi', params=params)
        
        results_list = search_results.get("results", [])
        
        # Apply genre filter
        if genre_filter:
            try:
                genre_id = int(genre_filter)
                filtered_results = [movie for movie in results_list if genre_id in movie.get("genre_ids", [])]
            except ValueError:
                filtered_results = results_list
        else:
            filtered_results = results_list 
        
        # Apply sort by filter  
        if sort_by == 'popularity.desc':
            filtered_results = sorted(filtered_results, key=lambda x: x.get('popularity', 0), reverse=True)
        elif sort_by == 'release_date.desc':
            filtered_results = sorted(filtered_results, key=lambda x: x.get('release_date', ''), reverse=True)
        elif sort_by == 'title':
            filtered_results = sorted(filtered_results, key=lambda x: x.get('title', '').lower())

        context = {
            'results': filtered_results,
            'query': query,
            'genres': get_tmdb_data('genre/movie/list', {'language': 'en-US'})['genres'],
            'tv_genres': get_tmdb_data('genre/tv/list', {'language': 'en-US'})['genres'],
            'selected_genre': genre_filter,
            'selected_sort': sort_by
        }

        return render(request, 'movies/search_results.html', context)
