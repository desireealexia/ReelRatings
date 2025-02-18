from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.utils.text import slugify
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
            
         # Save the movie data to the database
            for movie_data in movies_data:
                # Check if the movie already exists in the database
                movie, created = Movie.objects.get_or_create(
                    title=movie_data['title'],
                    defaults={
                        'release_date': movie_data['release_date'],
                        'description': movie_data['overview'],
                        'poster_url': "https://image.tmdb.org/t/p/w500" + movie_data['poster_path'],
                        'slug': slugify(movie_data['title'])
                    }
                )
                movies.append(movie)  # Add the saved movie to the list
            
            #  # Generate slug for each movie
            # for movie in movies_data:
            #     movie['slug'] = slugify(movie['title'])  # Generate slug for movie

            # movies = movies_data

    return render(request, 'movie_reviews/search_results.html', {'movies': movies, 'query': query})