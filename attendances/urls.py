from django.urls import path
from . import views

urlpatterns = [
    
    path('attendance/', views.attendance, name='attendance'),
    path('attendance/calculate/', views.calculate_attendance, name='calculate_attendance'),
    
]