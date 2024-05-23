from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recommend_destinations/', views.recommend_destinations, name='recommend_destinations'),
]
