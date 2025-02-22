from django.conf import settings
from django.conf.urls.static import static
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views import View
from .models import Review
from .forms import ReviewForm
from .utils import get_tmdb_data

urlpatterns = [
    # Your app URLs
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

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
        
        # Fetch user reviews for this movie
        reviews = Review.objects.filter(movie_id=movie_id)
        
        # Prepare the review form
        form = ReviewForm()
        
        context = {
            'movie': movie,
            'reviews': reviews,
            'recommendations': recommendations_list,
            'form': form,
        }
        
        return render(request, 'movies/movie_detail.html', context)

    def post(self, request, movie_id):
        # Ensure the user is logged in
        if not request.user.is_authenticated:
            return redirect('login')  # Redirect to login if user is not authenticated

        # Fetch movie details from TMDb API
        movie_data = get_tmdb_data(f'movie/{movie_id}', {'language': 'en-US'})
        movie_title = movie_data.get('title', '')

        # Process the review form submission
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user  # Associate the review with the logged-in user
            review.movie_id = movie_id
            review.movie_title = movie_title
            review.save()  # Save the review

            # Redirect to the same movie detail page after saving the review
            return redirect('movie_detail', movie_id=movie_id)

        # In case of an invalid form, re-render the page with the form
        context = {
            'movie': movie_data,
            'reviews': Review.objects.filter(movie_id=movie_id),
            'recommendations': get_tmdb_data(f"movie/{movie_id}/recommendations", {'language': 'en-US'}).get('results', []),
            'form': form,
        }

        return render(request, 'movies/movie_detail.html', context)
    
class TVShowDetailView(View):
    def get(self, request, series_id):
        show = get_tmdb_data(f"tv/{series_id}", {
            'language': 'en-US'
        })
        recommendations = get_tmdb_data(f"tv/{series_id}/recommendations", {'language': 'en-US'})
        
        recommendations_list = recommendations.get('results', [])
        
         # Fetch user reviews for this TV show
        reviews = Review.objects.filter(tv_show_id=series_id)
        
        # Prepare the review form
        form = ReviewForm()
        
        context = {
            'show': show,
            'reviews': reviews,
            'recommendations': recommendations_list,
            'form': form,
        }
        
        return render(request, 'movies/tv_show_detail.html', context)

    def post(self, request, series_id):
        # Ensure the user is logged in
        if not request.user.is_authenticated:
            return redirect('login')  # Redirect to login if user is not authenticated

        # Fetch TV show details from TMDb API
        show_data = get_tmdb_data(f'tv/{series_id}', {'language': 'en-US'})
        show_title = show_data.get('name', '')  # Get TV show title
        
        # Process the review form submission
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user  # Associate the review with the logged-in user
            review.tv_show_id = series_id
            review.tv_show_title = show_title
            review.save()  # Save the review

            # Redirect to the same TV show detail page after saving the review
            return redirect('tv_show_detail', series_id=series_id)

        # In case of an invalid form, re-render the page with the form
        context = {
            'show': show_data,
            'reviews': Review.objects.filter(tv_show_id=series_id),
            'recommendations': get_tmdb_data(f"tv/{series_id}/recommendations", {'language': 'en-US'}).get('results', []),
            'form': form,
        }

        return render(request, 'movies/tv_show_detail.html', context)
        
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