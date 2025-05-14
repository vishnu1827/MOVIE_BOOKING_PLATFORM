from django.contrib import admin
from .models import reviews
# Register your models here.

@admin.register(reviews)
class reviewsAdmin(admin.ModelAdmin):
    list_display = ['review_id', 'user', 'movie', 'rating', 'review_text', 'created_at']

