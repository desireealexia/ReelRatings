from django.conf import settings
from django.core.paginator import Paginator
from django.db.utils import IntegrityError
from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from datetime import datetime
from .models import Movie, Review, TVShow
import requests

# Create your views here.

TMDB_API_KEY = settings.TMDB_API_KEY
BASE_URL = 'https://api.themoviedb.org/3/'


def homepage(request):
    # Fetch Popular 5 Movies
    movie_response = requests.get(f'{BASE_URL}movie/popular?api_key={TMDB_API_KEY}&language=en-US&page=1')
    popular_movies = movie_response.json().get('results', [])[:5]

    # Fetch Popular 5 TV Shows
    tv_show_response = requests.get(f'{BASE_URL}tv/popular?api_key={TMDB_API_KEY}&language=en-US&page=1')
    popular_tv_shows = tv_show_response.json().get('results', [])[:5]

    return render(request, 'movie_reviews/homepage.html', {
        'popular_movies': popular_movies,
        'popular_tv_shows': popular_tv_shows
    })
    
def generate_unique_slug(model, title):
    """
    Generate a unique slug for a given model and title.
    """
    base_slug = slugify(title)
    unique_slug = base_slug
    counter = 1

    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = f"{base_slug}-{counter}"
        counter += 1

    return unique_slug

def search(request):
    query = request.GET.get('query', '')
    page_number = request.GET.get('page', 1)
    results = []
    
    if query:
        # Search for both movies and TV shows
        url = "https://api.themoviedb.org/3/search/multi"
        params = {
            'api_key': settings.TMDB_API_KEY,
            'query': query,
            'language': 'en-US',
            'page': 1
        }
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            search_results = response.json().get('results', [])
            
            for item in search_results:
                media_type = item.get('media_type')

                if media_type in ['movie', 'tv']:  # Only process movies and TV shows
                    title = item.get('title') if media_type == 'movie' else item.get('name')
                    release_date = item.get('release_date') if media_type == 'movie' else item.get('first_air_date')
                    description = item.get('overview', 'No description available')
                    poster_url = f"https://image.tmdb.org/t/p/w500{item['poster_path']}" if item.get('poster_path') else 'https://dummyimage.com/500x750/000000/ffffff.jpg&text=No+Image+Available'

                    # If release_date is empty, set it to None
                    if release_date == "":
                        release_date = None
                        
                    # Handle empty or invalid release dates
                    if release_date:
                        try:
                            release_date = datetime.strptime(release_date, '%Y-%m-%d').date()
                        except ValueError:
                            release_date = None

                    # Generate a unique slug
                    unique_slug = generate_unique_slug(Movie if media_type == 'movie' else TVShow, title)

                    try:
                        if media_type == 'movie':
                            obj, created = Movie.objects.get_or_create(
                                title=title,
                                defaults={
                                    'release_date': release_date,
                                    'description': description,
                                    'poster_url': poster_url,
                                    'slug': unique_slug
                                }
                            )
                        else:  # TV Show
                            obj, created = TVShow.objects.get_or_create(
                                title=title,
                                defaults={
                                    'release_date': release_date,
                                    'description': description,
                                    'poster_url': poster_url,
                                    'slug': unique_slug
                                }
                            )

                        results.append({
                            'title': title,
                            'release_date': release_date,
                            'description': description,
                            'poster_url': poster_url,
                            'media_type': media_type,
                            'slug': obj.slug
                        })

                    except IntegrityError:
                        print(f"Duplicate slug detected: {unique_slug}")
    
        # Pagination setup
        paginator = Paginator(results, 8)  # Show 12 results per page
        page_obj = paginator.get_page(page_number)  # Get the current page of results
        
        return render(request, 'movie_reviews/search_results.html', {
            'query': query,
            'results': page_obj.object_list,  # Use the page object's results
            'page_obj': page_obj,  # Pass the page object for pagination controls
        })

    return render(request, 'movie_reviews/search_results.html', {'query': query, 'results': results})

def movie_detail(request, slug):
    movie = get_object_or_404(Movie, slug=slug)
    reviews = Review.objects.filter(movie=movie)
    print("Movie Data:", movie.title, movie.poster_url)  # Debugging
    return render(request, 'movie_reviews/movie_detail.html', {
        'movie': movie,
        'reviews': reviews
    })
    
def tv_detail(request, slug):
    tv_show = get_object_or_404(TVShow, slug=slug)
    reviews = Review.objects.filter(tv_show=tv_show)
    return render(request, 'movie_reviews/tv_detail.html', {
        'tv_show': tv_show,
        'reviews': reviews
    })
    
def movie_list(request):
    """Fetches movies from TMDB API and displays them."""
    # Fetch movie data
    url = f"{BASE_URL}movie/popular?api_key={TMDB_API_KEY}&language=en-US&page=1"
    response = requests.get(url)
    movies = response.json().get('results', [])
    
    # Fetch all genres
    genre_url = f"{BASE_URL}genre/movie/list?api_key={TMDB_API_KEY}&language=en-US"
    genre_response = requests.get(genre_url)
    genres = genre_response.json().get('genres', [])
    
     # Create a mapping of genre_id to genre_name
    genre_dict = {genre['id']: genre['name'] for genre in genres}

    # Add genre names to each movie based on genre_ids
    for movie in movies:
        movie['genre_names'] = [genre_dict.get(genre_id, 'Unknown') for genre_id in movie['genre_ids']]

    return render(request, 'movie_reviews/movies.html', {'movies': movies})

def tv_show_list(request):
    """Fetches TV shows from TMDB API and displays them."""
    url = f"{BASE_URL}tv/popular?api_key={TMDB_API_KEY}&language=en-US&page=1"
    response = requests.get(url)
    tv_shows = response.json().get('results', [])
    
     # Fetch genres for TV shows
    genre_url = f"{BASE_URL}genre/tv/list?api_key={TMDB_API_KEY}&language=en-US"
    genre_response = requests.get(genre_url)
    genres = genre_response.json().get('genres', [])
    
    # Create a mapping of genre_id to genre_name
    genre_dict = {genre['id']: genre['name'] for genre in genres}

    # Add genre names to each TV show based on genre_ids
    for tv_show in tv_shows:
        tv_show['genre_names'] = [genre_dict.get(genre_id, 'Unknown') for genre_id in tv_show.get('genre_ids', [])]

    return render(request, 'movie_reviews/tv_shows.html', {'tv_shows': tv_shows})