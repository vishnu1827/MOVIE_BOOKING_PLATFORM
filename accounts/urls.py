from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerview, name='register'),
    path('home/', views.homeview, name='home'),
    path('login/', views.loginviews, name='login'),
    path('logout/', views.logoutview, name='logout'),
    
]