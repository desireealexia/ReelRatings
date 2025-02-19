from django.conf import settings
from django.core.paginator import Paginator
from django.db.utils import IntegrityError
from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from datetime import datetime
from .models import Movie, Review, TVShow
import requests

# Create your views here.
def homepage(request):
    return render(request, 'movie_reviews/homepage.html')

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