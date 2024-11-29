from django.urls import path
from . import views

urlpatterns = [
    
    path('authors/', views.authors, name='authors'),
    path('authors/add/', views.add_authors, name='add_authors'),
    path('teachers/', views.teachers, name='teachers'),
    path('teachers/add/', views.add_teachers, name='add_teachers'),
    path('auth/login/', views.user_login, name='user_login'),
    path('auth/logout/', views.user_logout, name='user_logout'),
    
]