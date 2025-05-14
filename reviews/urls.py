# reviews/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('movies/<slug:slug>/review/', views.submit_review, name='submit_review'),
]
