from django.shortcuts import render, redirect
from django.conf import settings
from bookings.models import bookings
import stripe
from payments.models import payments

# Create your views here.
def payment_page(request, booking_id):
    booking = bookings.objects.get(id=booking_id)
    if request.method == 'POST':
        booking = bookings.objects.get(id=booking_id)
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'inr',
                        'product_data': {
                            'name': 'Ticket Booking',
                        },
                        'unit_amount': int(booking.total_amount * 100), 
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            billing_address_collection='required',
            success_url = f'http://127.0.0.1:8000/payments/success/{booking.id}/',
            cancel_url = f'http://127.0.0.1:8000/payments/cancel/{booking.id}/'
        )
        return redirect(session.url, code=303)  
    return render(request, 'payments/payment.html', {
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'booking': booking,
        'movie': booking.movie,         
        'payment_success': True
    })  

def success(request, booking_id):
    user_booking = bookings.objects.get(id=booking_id)
    user_booking.booking_status = 'confirmed'
    user_booking.save()

    payments.objects.create(
        booking=user_booking,  # Use 'booking' here as it's singular now
        payment_method='card',
        amount=user_booking.total_amount,
        status='success'
    )

    return render(request, 'payments/success.html')


def cancel(request):
    booking=bookings.objects.get(id=booking_id)
    booking.booking_status='failed'
    booking.save()
    payments.objects.create(
        booking=booking,
        payment_method='card',
        amount=booking.total_amount,
        status='failed'
        )
    return render(request, 'payments/cancel.html')
