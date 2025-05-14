from django.urls import path

from . import views

urlpatterns = [
    path('movie/<slug>/', views.movie_view, name='movie_view')

]