import requests
from django.conf import settings

def get_tmdb_data(endpoint, params=None):
    base_url = "https://api.themoviedb.org/3"
    image_base_url = "https://image.tmdb.org/t/p/w500" 
    
    params = params or {}
    params['api_key'] = settings.TMDB_API_KEY
    response = requests.get(f"{base_url}/{endpoint}", params=params)
    data = response.json()
        
    # Add image base URL to each movie or TV show
    if 'results' in data:
        for item in data['results']:
            if 'poster_path' in item:
                item['poster_url'] = f"{image_base_url}{item['poster_path']}"
            else:
                item['poster_url'] = "https://dummyimage.com/500x750/000000/ffffff&text=No+Image+Available"  # Default image
    return data

def get_movie_details(movie_id):
    movie = get_tmdb_data(f"movie/{movie_id}", {'language': 'en-US'})
    credits = get_tmdb_data(f"movie/{movie_id}/credits", {'language': 'en-US'})

    if movie and credits:
        movie["cast"] = credits.get("cast", [])[:5]
        movie["directors"] = [member["name"] for member in credits.get("crew", []) if member.get("job") == "Director"]

    return movie

def get_tv_show_details(series_id):
    show = get_tmdb_data(f"tv/{series_id}", {'language': 'en-US'})
    credits = get_tmdb_data(f"tv/{series_id}/credits", {'language': 'en-US'})

    if show and credits:
        show["cast"] = credits.get("cast", [])[:5]  # Get top 5 cast members
        
    return show
