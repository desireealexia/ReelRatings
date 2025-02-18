from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.utils.text import slugify
from datetime import datetime
from .models import Movie, Review
import requests

# Create your views here.
def homepage(request):
    # Fetch all movies from the database
    movies = Movie.objects.all()
    return render(request, 'movie_reviews/homepage.html', {'movies': movies})

def movie_detail(request, slug):
    movie = get_object_or_404(Movie, slug=slug)
    reviews = Review.objects.filter(movie=movie)
    return render(request, 'movie_reviews/movie_detail.html', {
        'movie': movie,
        'reviews': reviews
    })

def search_movies(request):
    query = request.GET.get('query', '')
    movies = []

    if query:
        url = "https://api.themoviedb.org/3/search/movie"
        params = {
            'api_key': settings.TMDB_API_KEY,
            'query': query,
            'language': 'en-US',
            'page': 1
        }
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            movies_data = response.json().get('results', [])
            
            for movie_data in movies_data:
                # Get release_date from the API response or set it to None if missing or empty
                release_date = movie_data.get('release_date', None)

                # If release_date is empty, set it to None
                if release_date == "":
                    release_date = None
                
                # Check if the release date is in a valid format
                if release_date:
                    try:
                        release_date = datetime.strptime(release_date, '%Y-%m-%d').date()
                    except ValueError:
                        release_date = None  # If date format is invalid, set it to None

                movie, created = Movie.objects.get_or_create(
                    title=movie_data['title'],
                    defaults={
                        'release_date': release_date,
                        'description': movie_data.get('overview', 'No description available'),
                        'poster_url': "https://image.tmdb.org/t/p/w500" + (movie_data['poster_path'] if movie_data.get('poster_path') else ''),
                        'slug': slugify(movie_data['title'])
                    }
                )
                
                if created:  # If the movie was newly created, print it for debugging
                    print(f"Created new movie: {movie.title}")
                else:
                    print(f"Found existing movie: {movie.title}")
                
                movies.append(movie)  # Add the saved movie to the list
                
        else:
            print(f"Failed to fetch data from TMDb. Status code: {response.status_code}")

    return render(request, 'movie_reviews/search_results.html', {'movies': movies, 'query': query})