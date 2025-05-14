from django.contrib import admin
from .models import movies
# Register your models here.
@admin.register(movies)
class moviesAdmin(admin.ModelAdmin):
    list_display = ['movie_id', 'title', 'genre', 'language', 'synopsis', 'cast', 'duration_minutes', 'release_date', 'trailer_url', 'status']

