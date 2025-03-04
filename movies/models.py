from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.IntegerField(null=True, blank=True)
    tv_show_id = models.IntegerField(null=True, blank=True)
    movie_title = models.CharField(max_length=255, null=True, blank=True) 
    tv_show_title = models.CharField(max_length=255, null=True, blank=True)
    rating = models.IntegerField(choices=[(i, i) for i in range(1,6)])
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('movie_id', 'user')
        
    def __str__(self):
        if self.movie_id:
            return f"Review by {self.user.username} for '{self.movie_title}'"
        elif self.tv_show_id:
            return f"Review by {self.user.username} for '{self.tv_show_title}'"
        else:
            return f"Review by {self.user.username}"
    
class Watchlist(models.Model):
    watchlist_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.IntegerField()
    is_favourite = models.BooleanField(default=False)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-added_at']
        
    def __str__(self):
        return f"{self.user.username} - Movie ID {self.movie_id} {'(Favourite)' if self.is_favourite else ''}"