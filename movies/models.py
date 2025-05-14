from django.db import models

# Create your models here.
genre = [
    ['Action', 'Action'],
    ['Comedy', 'Comedy'],
    ['Drama', 'Drama'],
    ['Horror', 'Horror'],
    ['Romance', 'Romance'],
    ['Thriller', 'Thriller'],
    ['Sci-Fi', 'Sci-Fi'],
    ['Fantasy', 'Fantasy'],]
language = [
    ['English', 'English'],
    ['Hindi', 'Hindi'],
    ['Kannada', 'Kannada'],
    ['Tamil', 'Tamil'],
    ['Telugu', 'Telugu'],
    ['Malayalam', 'Malayalam'],
]
class movies(models.Model):
    movie_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=255, choices=genre)
    language = models.CharField(max_length=255, choices=language)
    synopsis = models.TextField()
    cast = models.TextField()
    movie_image = models.ImageField(upload_to='movie_image/', null=True, blank=True)
    duration_minutes = models.IntegerField()
    release_date = models.DateField()
    trailer_url = models.CharField(max_length=20000, null=True, blank=True)
    status = models.CharField()
    slug = models.CharField(max_length=1000, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = self.title.replace(" ", "-")
        super().save(*args, *kwargs)


    def __str__(self):
        return self.title