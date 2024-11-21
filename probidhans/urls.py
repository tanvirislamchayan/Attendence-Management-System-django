from django.urls import path
from . import views

urlpatterns = [
    
    path('probidhans/', views.probidhans, name='probidhans'),
    path('probidhans/add/', views.add_probidhans, name='add_probidhans'),
    
]