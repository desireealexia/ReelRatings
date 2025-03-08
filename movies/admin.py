from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Review

class ReviewAdmin(admin.ModelAdmin):
    """
    Lists fields for display in admin, fields for search,
    field filters, fields to pre-populate and rich-text editor.
    """
    list_display = ('review_id', 'user', 'movie_title', 'tv_show_title', 'rating', 'created_at')
    search_fields = ('movie_title', 'tv_show_title', 'review_text')
    list_filter = ('rating', 'created_at')
    
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        ('Personal info', {'fields': ('username', 'password','email', 'date_joined')}),
        )
    list_display = ('username', 'email', 'date_joined', 'is_active', 'is_staff')
    search_fields = ('username', 'email',)
    list_filter = ('is_active', 'is_staff')

# Register your models here.
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Review, ReviewAdmin)
