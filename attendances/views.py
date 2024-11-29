from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from departments.models import Department
from semesters.models import Semester
from subjects.models import Subject
from students.models import Student
from groups.models import Group
from .models import Attendance
from django.http import HttpResponseRedirect

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

    selected_department = req.GET.get('department', '')
    selected_semester = req.GET.get('semester', '')
    selected_subject = req.GET.get('subject', '')
    selected_date = req.GET.get('date', '')
    selected_group = req.GET.get('group', '')

    students = None
    subjects = None

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

    attendance_obj = None
    if selected_department and selected_semester and selected_subject and selected_date:        
        if not selected_group:
            attendance_obj = Attendance.objects.filter(
                department__slug = selected_department,
                semester__slug = selected_semester,
                subject__slug = selected_subject,
                date = selected_date,
            ).first()
        else:
            attendance_obj = Attendance.objects.filter(
                department__slug = selected_department,
                semester__slug = selected_semester,
                subject__slug = selected_subject,
                group__slug = selected_group,
                date = selected_date,
            ).first()    

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
        'attendance_obj': attendance_obj,
    }

    if attendance_obj and not teacher.is_author:  # Ensure proper handling of Attendance object
        messages.warning(req, f"Exists! You're not allowed to update please contact the Administrator.")
   


    if not attendance_obj and req.method == 'POST':
        student_list = req.POST.getlist('present')
        if students and selected_subject and selected_date:
            try:
                attendance_obj = Attendance.objects.create(
                    date=selected_date,
                    teacher=teacher,
                    subject=Subject.objects.get(slug=selected_subject),
                    semester=Semester.objects.get(slug=selected_semester),
                    department=Department.objects.get(slug=selected_department),
                    group=Group.objects.get(slug=selected_group) if selected_group else None,
                )

                present_students = students.filter(uid__in=student_list)
                absent_students = students.exclude(uid__in=student_list)
                print(f'present {present_students}')
                print(f'absent {absent_students}')

                attendance_obj.student_presents.add(*present_students)
                attendance_obj.student_absents.add(*absent_students)
                attendance.save()

                # context.update()
                messages.success(req, "Attendance recorded successfully!")
                referer_url = req.META.get('HTTP_REFERER', req.path_info)
                return redirect(referer_url)
                

            except Exception as e:
                messages.warning(req, f'Error while creating the entry: {e}')
                referer_url = req.META.get('HTTP_REFERER', req.path_info)
                return redirect(referer_url)
    
    if attendance_obj and teacher.is_author and req.method == 'POST':
        student_list = req.POST.getlist('present')
        present_students = students.filter(uid__in=student_list)
        absent_students = students.exclude(uid__in=student_list)
        print(f'present {present_students}')
        print(f'absent {absent_students}')

        attendance_obj.student_presents.add(*present_students)
        attendance_obj.student_absents.add(*absent_students)
        attendance_obj.save()

        messages.info(req, 'Updated Entry Successfully.')
        referer_url = req.META.get('HTTP_REFERER', req.path_info)
        return redirect(referer_url)



    return render(req, 'attendance/attendance.html', context)




# check attendance
def check_attendance(department, semester, subject, date, group):
    attendance_obj = None
    if department and semester and subject and date:        
        if not group:
            attendance_obj = Attendance.objects.filter(
                department__slug = department,
                semester__slug = semester,
                subject__slug = subject,
                date = date,
            ).first()
        else:
            attendance_obj = Attendance.objects.filter(
                department__slug = department,
                semester__slug = semester,
                subject__slug = subject,
                group__slug = group,
                date = date,
            ).first()
    if attendance_obj:
        print(attendance_obj)
        return attendance_obj
    else:
        print('No attendance')
        return False

def calculate_attendance(request):
    context = {
        'page': 'Attendance Calculation'
    }
    return render(request, 'attendance/atd_calculation.html', context)