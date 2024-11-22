from django.urls import path
from . import views

urlpatterns = [
    
    path('groups/', views.groups, name='groups'),
    path('groups/add/', views.add_groups, name='add_groups'),
    
]