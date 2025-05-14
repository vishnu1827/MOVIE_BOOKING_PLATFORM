from django.urls import path
from . import views

urlpatterns = [
    path('showtime/<slug:slug>/seating/<int:showtime_id>/', views.seat_selection_view, name='seating'),
    path('showtime/<slug:slug>/', views.theatre_show_time_view, name='showtime'),
    path('showtime/<slug:slug>/<str:date_str>/', views.theatre_show_time_selected_date_view, name='theatre_show_time_selected_date'),
    path('bookings/book/<int:showtime_id>/', views.book_ticket_view, name='book_ticket'),
    path('cancel_ticket/<int:booking_id>/', views.cancel_ticket, name='cancel_ticket'),
]
