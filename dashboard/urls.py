from django.urls import path
from .views import movies_listview
from .views import movies_by_genre
from .views import your_orders

urlpatterns = [
    path('movies/', movies_listview, name='movies_list'),
    path('genre/<str:genre>/', movies_by_genre, name='movies_by_genre'),
    path('your_orders/', your_orders, name='your_orders'),
    
]
