from django.shortcuts import render
from movies.models import movies
from django.http import JsonResponse
from accounts.models import User
from django.contrib.auth.decorators import login_required
from payments.models import payments
from bookings.models import bookings, bookingseats
# Create your views here.


def movies_listview(request):
    query = request.GET.get('q', '')
    if query:
        movie_list = movies.objects.filter(title__icontains=query)
    else:
        movie_list = movies.objects.all()
    
    context = {
        'movies': movie_list,
        'search_query': query,  # optional: useful to repopulate search box
    }
    return render(request, 'movies/movies.html', context)

def movies_by_genre(request, genre):
    movie_list = movies.objects.filter(genre__iexact=genre)
    return render(request, 'movies/movies.html', {
        'movies': movie_list,
        'selected_genre': genre,
    })

@login_required
def your_orders(request):
    user = User.objects.get(username=request.user)
    user_bookings = bookings.objects.filter(user=user, booking_status='confirmed').order_by('-booking_time')
    
    tickets = {}
    for booking in user_bookings:
        try:
            payment = payments.objects.get(booking=booking)
        except payments.DoesNotExist:
            continue

        seats = bookingseats.objects.filter(booking=booking)

        # Safely get show_time
        showtime = getattr(booking, 'showtime', None)
        show_time_value = getattr(showtime, 'show_time', None)

        if show_time_value:
            can_cancel = check_cancellation(show_time_value)
        else:
            can_cancel = False  # or True, based on your logic

        tickets[payment] = {'seats': seats, 'can_cancel': can_cancel}
    
    context = {
        'movies': movies.objects.all(),
        'tickets': tickets,
        'user': user,
    }

    return render(request, 'dashboard/your_orders.html', context)

from datetime import timedelta
from django.utils.timezone import now

def check_cancellation(show_time):
    now_time = now()  # Get the current time
    buffer_time = show_time - timedelta(minutes=20)  # 20 minutes before showtime
    return now_time < buffer_time  # Return True if current time is before the buffer time
