from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.text import slugify

# Create your models here.
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=200, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-date_joined"] 
    
class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    movie_id = models.IntegerField(null=True, blank=True)
    tv_show_id = models.IntegerField(null=True, blank=True)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Review by {self.user.username} for Movie ID {self.movie_id or 'N/A'}"
    
class Watchlist(models.Model):
    watchlist_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    movie_id = models.IntegerField()
    is_favourite = models.BooleanField(default=False)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-added_at']
        
    def __str__(self):
        return f"{self.user.username} - Movie ID {self.movie_id} {'(Favourite)' if self.is_favourite else ''}"