from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from departments.models import Department
from semesters.models import Semester
from subjects.models import Subject
from students.models import Student
from groups.models import Group

# Create your views here.

# attendance
def attendance(req):
    if not req.user.is_authenticated:
        messages.warning(req, 'Login First !')
        return redirect('user_login')

    teacher = getattr(req.user, 'teacher', None)
    if not teacher:
        messages.warning(req, 'You are not authorized to access this page.')
        return redirect('user_login')

    # Retain existing query parameters
    selected_department = req.GET.get('department', '')
    selected_semester = req.GET.get('semester', '')
    selected_subject = req.GET.get('subject', '')
    selected_date = req.GET.get('date', '')
    selected_group = req.GET.get('group', '')

    students = None
    subjects = None

    # Fetch students and subjects if department and semester are selected
    if selected_department and selected_semester:
        student_filter = {
            'department__slug': selected_department,
            'semester__slug': selected_semester,
        }
        if selected_group:
            student_filter['group__slug'] = selected_group

        students = Student.objects.filter(**student_filter).order_by('roll')
        subjects = Subject.objects.filter(
            department__slug=selected_department,
            semester__slug=selected_semester,
        )

    context = {
        'page': 'Attendance',
        'teacher': teacher,
        'departments': Department.objects.all().order_by('name'),
        'semesters': Semester.objects.all().order_by('name'),
        'groups': Group.objects.all().order_by('name'),
        'selected_department': selected_department,
        'selected_semester': selected_semester,
        'selected_subject': selected_subject,
        'selected_date': selected_date,
        'selected_group': selected_group,
        'students': students,
        'subjects': subjects,
    }
    print(context)

    return render(req, 'attendance/attendance.html', context)


def calculate_attendance(request):
    context = {
        'page': 'Attendance Calculation'
    }
    return render(request, 'attendance/atd_calculation.html', context)