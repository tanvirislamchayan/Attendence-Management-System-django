from django.urls import path
from . import views

urlpatterns = [
    
    path('subjects/', views.subjects, name='subjects'),
    path('subjects/add/', views.add_subjects, name='add_subjects'),
    
]