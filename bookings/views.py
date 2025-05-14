from django.shortcuts import render, redirect, HttpResponse
from theatre.models import theatre, showtimes, seats
from movies.models import movies
from accounts.models import User
from datetime import datetime, timedelta
from .models import bookings, bookingseats
from django.contrib import messages
import json
from django.conf import settings
import stripe
from django.contrib.auth.decorators import login_required

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.

def theatre_show_time_view(request, slug):
    today = datetime.today().date()
    start_date = today-timedelta(days=0)
    week=[]
    for i in range(7):
        day=start_date+timedelta(days=i)
        week.append({
            'name' : day.strftime('%a').upper(),
            'day' : day.day,
            'month' : day.strftime('%b').upper(),
            'date' : day

        })



    if movies.objects.filter(slug=slug).exists():
        movie = movies.objects.get(slug=slug)
        theatre_showtimes=[
            showtimes.objects.filter(movie=movie, theatre=theatre_obj).order_by('show_time')
            for theatre_obj in theatre.objects.all() if showtimes.objects.filter(movie=movie, theatre=theatre_obj).exists()]
        context = {
            'theatre_showtimes': theatre_showtimes,
            'm': movie,
            'week': week,
            'today': today,

        }
        return render(request, 'theatre/theatre_show_time.html', context)
    return render(request, 'movies/404.html' )    


def theatre_show_time_selected_date_view(request, slug, date_str):
    try:
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        selected_date = datetime.today().date()

    today = datetime.today().date()
    week = []
    for i in range(7):
        day = today + timedelta(days=i)
        week.append({
            'name': day.strftime('%a').upper(),
            'day': day.day,
            'month': day.strftime('%b').upper(),
            'date': day
        })

    movie = movies.objects.filter(slug=slug).first()
    if not movie:
        context = {
            'week': week,
            'today': selected_date,
            'theatre_showtimes': [],
            'm': None,
        }
        return render(request, 'theatre/theatre_show_time.html', context)

    theatre_showtimes = []
    for theatre_obj in theatre.objects.all():
        shows = showtimes.objects.filter(
            movie=movie,
            theatre=theatre_obj,
            show_time__date=selected_date
        ).order_by('show_time')
        if shows.exists():
            theatre_showtimes.append(shows)

    context = {
        'theatre_showtimes': theatre_showtimes,
        'week': week,
        'today': selected_date,
        'm': movie,
    }

    return render(request, 'theatre/theatre_show_time.html', context)

def seat_selection_view(request, slug, showtime_id):
    showtime = showtimes.objects.get(id=showtime_id)

    # Get all seats for this showtime's screen
    all_seats = seats.objects.filter(
        theatre=showtime.theatre,
        screen_number=showtime.screen_number
    ).order_by('row_label', 'seat_number')

    # Get IDs of booked seats
    booked_seats = bookingseats.objects.filter(
        booking__showtime=showtime,
        booking__booking_status='confirmed'
    )
    booked_seat_ids = [seat.seat.id for seat in booked_seats]

    # Group ALL seats (not just available) by row
    seat_rows = {}
    for seat in all_seats:
        row = seat.row_label
        if row not in seat_rows:
            seat_rows[row] = []
        seat_rows[row].append(seat)

    vip_rows = ['A', 'B', 'C']
    gold_rows = ['D', 'E', 'F']
    silver_rows = [row for row in seat_rows if row not in vip_rows + gold_rows]

    context = {
        'showtime': showtime,
        'slug': slug,
        'seat_rows': seat_rows,
        'booked_seats': booked_seat_ids,  # Just the IDs of booked ones
        'vip_rows': vip_rows,
        'gold_rows': gold_rows,
        'silver_rows': silver_rows,
    }
    return render(request, 'theatre/seating.html', context)


@login_required
def book_ticket_view(request, showtime_id):
    if request.method == 'POST':
        selected_seats = json.loads(request.POST.get('selected_seats'))  # ⬅️ use () not []
        total_amount = int(request.POST.get('total_amount'))

        showtime = showtimes.objects.get(id=showtime_id)
        user = request.user
        booking = bookings.objects.create(
            user=user,
            showtime=showtime,
            total_amount=total_amount,
            booking_status='pending'
        )

        for seat in selected_seats:
            seat_key = seat['key']
            row = seat_key[0]
            number = seat_key[1:]
            seat_obj = seats.objects.get(row_label=row,seat_number=number,screen_number=showtime.screen_number,theatre=showtime.theatre)
            bookingseats.objects.create(booking=booking, seat=seat_obj)

        context = {
            'convenience_fee': 49,
            'total_amount': total_amount,
            'booking': booking,
            'tickets': [s['key'] for s in selected_seats],
            'showtime': showtime,
            'subtotal': total_amount + 49,
            'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
            
        }
        return render(request, 'payments/proceed_payments.html', context)

    return HttpResponse("Invalid Request", status=400)



@login_required
def cancel_ticket(request, booking_id):
    booking = bookings.objects.get(id=booking_id)
    booking.booking_status = 'cancelled'
    booking.save()
    qs = bookingseats.objects.filter(booking=booking)
    qs.delete()
    messages.error(request, 'Your booking has been cancelled')
    return redirect('your_orders')
