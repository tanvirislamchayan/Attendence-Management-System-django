from django.urls import path
from . import views

urlpatterns = [
    
    path('sessions/', views.sessions, name='sessions'),
    path('sessions/add/', views.add_sessions, name='add_sessions'),
    
]