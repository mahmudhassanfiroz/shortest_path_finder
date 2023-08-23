
from django.urls import path
from .views import find_shortest_distance

urlpatterns = [
    path('', find_shortest_distance, name='find_shortest_distance'),
]