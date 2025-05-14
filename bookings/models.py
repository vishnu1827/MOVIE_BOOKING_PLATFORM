from django.db import models
from accounts.models import User
from theatre.models import theatre, showtimes, seats
# Create your models here.


class bookings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    showtime = models.ForeignKey(showtimes, on_delete=models.SET_NULL, null=True, blank=True)
    booking_time= models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    booking_status = models.CharField(max_length=20, choices=[['booked', 'booked'], ['cancelled', 'cancelled'],['pending', 'pending']]) 

class bookingseats(models.Model):
    booking = models.ForeignKey(bookings, on_delete=models.CASCADE)
    seat = models.ForeignKey(seats, on_delete=models.SET_NULL, null=True, blank=True)