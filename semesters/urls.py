from django.urls import path
from . import views

urlpatterns = [
    
    path('semesters/', views.semesters, name='semesters'),
    path('semesters/add/', views.add_semesters, name='add_semesters'),
    
]