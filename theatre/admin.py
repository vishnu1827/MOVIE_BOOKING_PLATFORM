from django.contrib import admin
from .models import theatre, showtimes, seats


# Register your models here.

@admin.register(theatre)
class theatreAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'address', 'manager']

@admin.register(showtimes)
class showtimesAdmin(admin.ModelAdmin):
    list_display = ['movie', 'theatre', 'show_time', 'screen_number']

@admin.register(seats)
class seatsAdmin(admin.ModelAdmin):
    list_display = ['theatre', 'screen_number', 'row_label', 'seat_number', 'seat_type']

    

