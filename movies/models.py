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
    
    class Meta:
        ordering = ["-date_joined"] # Shows newest users first
    
class Movie(models.Model):
    movie_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    release_date = models.DateField(null=True, blank=True)
    description = models.TextField()
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    poster_url = models.CharField(blank=True, null=True)
    slug = models.SlugField(max_length=200, unique=True)
    
    genres = models.ManyToManyField('Genre', through='MovieGenre', related_name='movies')

    class Meta:
        ordering = ["average_rating", "-release_date"]
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            
            original_slug = self.slug
            counter = 1
            while Movie.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.title

class TVShow(models.Model):
    show_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    poster_path = models.CharField(max_length=255)
    release_date = models.DateField(null=True, blank=True)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    poster_url = models.CharField(blank=True, null=True)
    slug = models.SlugField(max_length=200, unique=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.title
    
class Genre(models.Model):
    genre_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, blank=True)
    
    class Meta:
        ordering = ["name"]
    
class MovieGenre(models.Model):
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)

class Person(models.Model):
    person_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    
class MovieCast(models.Model):
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.CharField(max_length=200)
        
    def __str__(self):
        return f"{self.person.name} as {self.role} in {self.movie.title}"
    
class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    movie = models.ForeignKey('Movie', null=True, blank=True, on_delete=models.CASCADE)
    tv_show = models.ForeignKey('TVShow', null=True, blank=True, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)]) # Rating between 1 and 5
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Review for {self.movie or self.tv_show}"
    
class Watchlist(models.Model):
    watchlist_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    is_favourite = models.BooleanField(default=False) # Shows if movie/TV show is favourite
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-added_at']
        
    def __str__(self):
        return f"{self.user.username} - {self.movie.title} {'(Favourite)' if self.is_favourite else ''}"