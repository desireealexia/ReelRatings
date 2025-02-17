from django.contrib import admin
from .models import User, Movie, Genre, MovieGenre, Person, MovieCast, Review, Watchlist

# Custom admin for Movie model
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'release_date', 'average_rating']
    search_fields = ['title', 'description']
    list_filter = ['release_date']

# Register your models here.
admin.site.register(User)
admin.site.register(Movie, MovieAdmin) # Register the Movie model with the custom admin
admin.site.register(Genre)
admin.site.register(MovieGenre)
admin.site.register(Person)
admin.site.register(MovieCast)
admin.site.register(Review)
admin.site.register(Watchlist)
