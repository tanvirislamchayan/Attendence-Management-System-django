from django.urls import path
from . import views

urlpatterns = [
    
    path('students/', views.students, name='students'),
    path('students/add/', views.add_students, name='add_students'),
    path('students/add/by-form', views.add_students_by_form, name='add_students_by_form'),
    path('students/add/by-xlsx', views.add_by_xlsx, name='add_by_xlsx'),
    
]