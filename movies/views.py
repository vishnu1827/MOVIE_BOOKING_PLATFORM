from django.shortcuts import render
from django.db.models import Avg
from movies.models import movies
from reviews.models import reviews

# Create your views here.

def movie_view(request, slug):
    if movies.objects.filter(slug=slug).exists():
        movie=movies.objects.get(slug=slug)
        if reviews.objects.filter(movie=movie).exists():
            review=reviews.objects.filter(movie=movie)
            no_users=review.count()
            rating=review.aggregate(avg_rating=Avg('rating'))
            
        

            context={
            'movie': movie,
            'rating': rating['avg_rating'],
            'no_users': no_users,
            'reviews': review,
           
            }
            return render(request, 'movies/movie.html', context)
    return render(request, 'movies/404.html',status=404)



