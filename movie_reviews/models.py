from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.text import slugify

# Create your models here.
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=200, unique=True) # ensures that no two users can have the same username
    email = models.EmailField(unique=True) # ensures that no two users can have the same email
    password = models.CharField(max_length=200)
    date_joined = models.DateTimeField(auto_now_add=True)
    
class Movie(models.Model):
    movie_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    release_date = models.DateField()
    description = models.TextField()
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True) # Nullable before rating
    poster_url = models. CharField(max_length=250)
    slug = models.SlugField(unique=True, blank=True)  # Keep blank=True for automatic slug generation
    
    def save(self, *args, **kwargs):
        if not self.slug:  # Generate slug only if it doesn't already exist
            self.slug = slugify(self.title)
        super(Movie, self).save(*args, **kwargs)

class Genre(models.Model):
    genre_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    
class MovieGenre(models.Model):
    movie = models. ForeignKey('Movie', on_delete=models.CASCADE)
    genre = models. ForeignKey('Genre', on_delete=models.CASCADE)

class Person(models.Model):
    person_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    
class MovieCast(models.Model):
    movie = models. ForeignKey('Movie', on_delete=models.CASCADE)
    person = models. ForeignKey('Person', on_delete=models.CASCADE)
    role = models.CharField(max_length=200)
    
class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    user = models. ForeignKey('User', on_delete=models.CASCADE)
    movie = models. ForeignKey('Movie', on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)]) # Rating between 1 and 5
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
class Watchlist(models.Model):
    watchlist_id = models.AutoField(primary_key=True)
    user = models. ForeignKey('User', on_delete=models.CASCADE)
    movie = models. ForeignKey('Movie', on_delete=models.CASCADE)
    is_favourite = models.BooleanField(default=False) # Shows if movie/TV show is favourite
    added_at = models.DateTimeField(auto_now_add=True)