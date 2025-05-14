from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import reviews
from movies.models import movies
from django.contrib.auth.decorators import login_required

@login_required
def submit_review(request, slug):
    movie = movies.objects.filter(slug=slug).first()

    if not movie:
        return HttpResponse("Movie not found.", status=400)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        review_text = request.POST.get('review_text')


        reviews.objects.create(
            user=request.user,
            movie=movie,
            rating=rating,
            review_text=review_text
        )

        return redirect('movie_view', slug=slug)

    return render(request, 'reviews/submit_review.html', {'movie': movie})
