from django.contrib import admin
from .models import User, Review, Watchlist

# Register your models here.
admin.site.register(User)
admin.site.register(Review)
admin.site.register(Watchlist)
