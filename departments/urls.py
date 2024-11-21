from django.urls import path
from . import views

urlpatterns = [
    
    path('departments/', views.departments, name='departments'),
    path('departments/add/', views.add_departments, name='add_departments'),
    
]