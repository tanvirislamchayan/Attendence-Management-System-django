from django.shortcuts import render, redirect
from teachers.models import Teacher
from departments.models import Department
from semesters.models import Semester
from session.models import Session
from probidhans.models import Probidhan
from groups.models import Group
from subjects.models import Subject
from students.models import Student
from django.contrib import messages


# Create your views here.

# home
def home(request):
    context = {
        'page': 'Dashboard'
    }

    if not request.user.is_authenticated:
        messages.warning(request, 'Login First!!')
        return redirect('user_login')
    
    authors = Teacher.objects.filter(is_author = True, is_active=True, is_teacher=True).count()
    teachers = Teacher.objects.filter(is_active=True, is_teacher=True).count()
    departments = Department.objects.all().count()
    semesters = Semester.objects.all().count()
    sessions = Session.objects.all().count()
    probidhans = Probidhan.objects.all().count()
    groups = Group.objects.all().count()
    subjects = Subject.objects.all().count()
    students = Semester.objects.all().count()

    context.update({
        'authors': authors,
        'teachers': teachers,
        'departments': departments,
        'semesters': semesters,
        'sessions': sessions,
        'probidhans': probidhans,
        'groups': groups,
        'subjects': subjects,
        'students': students,
    })

    return render(request, 'home/index.html', context)