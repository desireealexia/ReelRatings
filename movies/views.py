from django.db.models import Avg 
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views import View
from .models import Review
from .forms import ReviewForm
from .utils import get_tmdb_data, get_movie_details, get_tv_show_details


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
        movie = get_movie_details(movie_id)
        recommendations = get_tmdb_data(f"movie/{movie_id}/recommendations", {'language': 'en-US'}).get('results', [])
        
        # Fetch user reviews for this movie
        reviews = Review.objects.filter(movie_id=movie_id).order_by("-created_at")
        
        form = ReviewForm()
        
        # Calculate average rating
        average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        
        # Paginate for recommendations section (4 per page)
        paginator = Paginator(recommendations, 4) 
        page_number = request.GET.get('page')
        recommendations_page = paginator.get_page(page_number)
        
        context = {
            'movie': movie,
            'reviews': reviews,
            'average_rating': average_rating,
            'recommendations': recommendations_page,
            "cast": movie.get("cast", []),
            "directors": movie.get("directors", []),
            'form': form,
        }
        
        return render(request, 'movies/movie_detail.html', context)
    
    def post(self, request, movie_id):
        movie_data = get_tmdb_data(f"movie/{movie_id}")
        movie_title = movie_data.get('title', 'Unknown Title')
        
        form = ReviewForm(request.POST)
        
        if form.is_valid():
            review, created = Review.objects.update_or_create(
                movie_id=int(movie_id),
                user=request.user,
                defaults={
                    'rating': form.cleaned_data['rating'],
                    'review_text': form.cleaned_data['review_text'],
                    'movie_title': movie_title,
                }
            )
            if created:
                messages.success(request, "Your review has been submitted!")
            else:
                messages.info(request, "You already submitted a review for this movie.")
            
            return redirect('movie_detail', movie_id=movie_id)

        # If the form isn't valid, reload the page with errors
        reviews = Review.objects.filter(movie_id=movie_id)
        avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0

        context = {
            'movie': movie_data,
            'reviews': reviews,
            'avg_rating': round(avg_rating, 1),
            'form': form,
        }
        return render(request, 'movies/movie_detail.html', context)
    
class TVShowDetailView(View):
    def get(self, request, series_id):
        show = get_tv_show_details(series_id)
        recommendations = get_tmdb_data(f"tv/{series_id}/recommendations", {'language': 'en-US'}).get('results', [])

        # Fetch user reviews for this TV show
        reviews = Review.objects.filter(tv_show_id=series_id).order_by("-created_at")
        
        form = ReviewForm()
        
        # Calculate average rating
        average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        
        # Paginate for recommendations section (4 per page)        
        paginator = Paginator(recommendations, 4)
        page_number = request.GET.get('page')
        recommendations_page = paginator.get_page(page_number)
        
        context = {
            'show': show,
            'reviews': reviews,
            'average_rating': average_rating,
            'recommendations': recommendations_page,
            "cast": show.get("cast", []),
            'form': form,
        }
        
        return render(request, 'movies/tv_show_detail.html', context)
    
    def post(self, request, series_id):
        show_data = get_tmdb_data(f"tv/{series_id}")
        show_title = show_data.get('name', 'Unknown Title')
        
        form = ReviewForm(request.POST)
        
        if form.is_valid():
            review, created = Review.objects.update_or_create(
                tv_show_id=int(series_id),
                user=request.user,
                defaults={
                    'rating': form.cleaned_data['rating'],
                    'review_text': form.cleaned_data['review_text'],
                    'tv_show_title': show_title,
                }
            )
            
            if created:
                messages.success(request, "Your review has been submitted!")
            else:
                messages.info(request, "You already submitted a review for this TV show.")
            
            return redirect('tv_show_detail', series_id=series_id)
        
        # Debugging form errors
        print(f"Form errors: {form.errors}")

        # If the form isn't valid, reload the page with errors
        reviews = Review.objects.filter(tv_show_id=series_id)
        avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0

        context = {
            'show': show_data,
            'reviews': reviews,
            'avg_rating': round(avg_rating, 1),
            'form': form,
        }
        return render(request, 'movies/tv_show_detail.html', context)
        
class SearchResultsView(View):
    def get(self, request):
        query = request.GET.get('q', '')  # Get search query
        genre_filter = request.GET.get('genre', '')  # Get genre filter
        sort_by = request.GET.get('sort', 'popularity.desc')  # Default sort by popularity
        page_number = request.GET.get('page', 1) # Get page number from query params

        params = {
            'query': query,
            'language': 'en-US',
            'page': page_number,
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

        # Paginate the filtered results
        paginator = Paginator(filtered_results, 12)  # 10 results per page
        page_obj = paginator.get_page(page_number)
        
        context = {
            'results': page_obj,
            'query': query,
            'genres': get_tmdb_data('genre/movie/list', {'language': 'en-US'})['genres'],
            'tv_genres': get_tmdb_data('genre/tv/list', {'language': 'en-US'})['genres'],
            'selected_genre': genre_filter,
            'selected_sort': sort_by,
        }

        return render(request, 'movies/search_results.html', context)