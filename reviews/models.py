from django.db import models
from accounts.models import User
from movies.models import movies

# Create your models here.

class reviews(models.Model):
    review_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(movies, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
