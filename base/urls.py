from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('', views.home, name="home"),
    path('team/<str:pk>/', views.team, name="team"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),

    path('create-team/', views.createTeam, name="create-team"),
    path('update-team/<str:pk>/', views.updateTeam, name="update-team"),
    path('delete-team/<str:pk>/', views.deleteTeam, name="delete-team"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),

    path('update-user/', views.updateUser, name="update-user"),

    path('projects/', views.projectsPage, name="projects"),
    path('activity/', views.activityPage, name="activity"),
    
    path('incident/<str:pk>/', views.incidentsPage, name="incident"),
]
