from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Review, Watchlist

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        ('Personal info', {'fields': ('username', 'password','email', 'date_joined')}),
    )

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Register your models here.
admin.site.register(Review)
admin.site.register(Watchlist)
