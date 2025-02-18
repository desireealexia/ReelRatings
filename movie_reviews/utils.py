from django.conf import settings
import requests

def fetch_tmdb_movie_data(query):
    url = f'https://api.themoviedb.org/3/search/movie'
    params = {
        'api_key': settings.TMDB_API_KEY,
        'query': query,
        'language': 'en-US',
        'page': 1
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json().get('results', [])
    else:
        return []
