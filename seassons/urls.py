from django.urls import path
from . import views

urlpatterns = [
    
    path('seassons/', views.seassons, name='seassons'),
    path('seassons/add/', views.add_seassons, name='add_seassons'),
    
]