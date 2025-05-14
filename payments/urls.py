from django.urls import path
from . import views

urlpatterns = [
    path('payment/<int:booking_id>/', views.payment_page, name='payment'),
    path('success/<int:booking_id>/', views.success, name='payment_success'),
    path('cancel/<int:booking_id>/', views.cancel, name='payment_cancel'),
]