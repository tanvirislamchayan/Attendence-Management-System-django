from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    
    path('authors/', views.authors, name='authors'),
    path('authors/add/', views.add_authors, name='add_authors'),
    path('teachers/', views.teachers, name='teachers'),
    path('teachers/add/', views.add_teachers, name='add_teachers'),
    
]