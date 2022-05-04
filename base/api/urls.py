from django.urls import path
from . import views

urlpatterns = [
    path('',  views.getRoutes),
    path('teams/', views.getTeam),
    path('teams/<str:pk>/', views.getTeam),
    path('users/', views.getUser),
    path('users/<str:pk>/', views.getUser)
]
