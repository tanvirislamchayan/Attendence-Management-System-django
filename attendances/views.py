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
from datetime import datetime
from calendar import monthrange
from django.db.models import Q

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
                # attendance.save()

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

        attendance_obj.student_presents.clear()
        attendance_obj.student_absents.clear()

        attendance_obj.student_presents.add(*present_students)
        attendance_obj.student_absents.add(*absent_students)
        # attendance_obj.save()

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
    departments = Department.objects.all()
    semesters = Semester.objects.all()
    months = []
    attendance_objs = Attendance.objects.all().order_by('-id')
    for obj in attendance_objs:
        if not obj.month in months:
            months.append(obj.month)
    context = {
        'page': 'Attendance Summary',
        'departments': departments,
        'semesters': semesters,
        'months': months,
    }
    attendance_data = None
    if request.method == 'POST':
        cal_type = request.POST.get('cal_type')
        if cal_type == 'day':
            d_department = request.POST.get('d_department', '') 
            d_semester = request.POST.get('d_semester', '') 
            d_date = request.POST.get('d_date', '') 

            attendance_data = calculate_day(d_department, d_semester, d_date)
            request.session['d_date'] = d_date
            request.session['d_semester'] = d_semester
            request.session['d_department'] = d_department
            request.session['attendance_summary'] = attendance_data
        
        elif cal_type == 'month':
            m_department = request.POST.get('m_department', '')
            m_semester = request.POST.get('m_semester', '')
            m_month = request.POST.get('m_month', '')

            attendance_data = calculate_month(m_department, m_semester, m_month)
            request.session['m_month'] = m_month
            request.session['m_semester'] = m_semester
            request.session['m_department'] = m_department
            request.session['attendance_summary'] = attendance_data

        elif cal_type == 'semester':
            s_department = request.POST.get('s_department', '')
            s_semester = request.POST.get('s_semester', '')
            s_month_start = request.POST.get('s_month_start', '')
            s_month_end = request.POST.get('s_month_end', '')

            attendance_data = calculate_semester(s_department, s_semester, s_month_start, s_month_end)
            if "error" in attendance_data:
                messages.warning(request, attendance_data["error"])
                return redirect(request.META.get('HTTP_REFERER', request.path_info))

            request.session['s_month_start'] = s_month_start
            request.session['s_month_end'] = s_month_end
            request.session['s_department'] = s_department
            request.session['s_semester'] = s_semester
            request.session['attendance_summary'] = attendance_data


        referer_url = request.META.get('HTTP_REFERER', request.path_info)
        return redirect(referer_url)

    # Retrieve data from session
    if 'attendance_summary' in request.session:
        context.update({
            'attendance_summary': request.session.pop('attendance_summary'),
        })
        if 'd_date' in request.session:
            # Day-wise attendance
            context.update({
                'sel_dep': request.session.pop('d_department'),
                'sel_sem': request.session.pop('d_semester'),
                'sel_date': request.session.pop('d_date'),
            })
        elif 'm_month' in request.session:
            # Month-wise attendance
            context.update({
                'sel_dep': request.session.pop('m_department'),
                'sel_sem': request.session.pop('m_semester'),
                'sel_month': request.session.pop('m_month'),
            })
        elif 's_month_start' in request.session and 's_month_end' in request.session:
            # Semester-wise attendance
            context.update({
                'sel_dep': request.session.pop('s_department'),
                'sel_sem': request.session.pop('s_semester'),
                'sel_month_start': request.session.pop('s_month_start'),
                'sel_month_end': request.session.pop('s_month_end'),
            })

    if 'sel_dep' and 'sel_sem' in context:
        sel_dep = context.get('sel_dep')
        sel_sem = context.get('sel_sem')
        sel_dep_name = Department.objects.get(id=sel_dep)
        sel_sem_name = Semester.objects.get(id=sel_sem)
        context.update({
            'sel_dep_name': sel_dep_name,
            'sel_sem_name': sel_sem_name,
        })

    return render(request, 'attendance/atd_calculation.html', context)


def calculate_day(d_department, d_semester, d_date):
    department_obj = Department.objects.get(id=d_department)
    semester_obj = Semester.objects.get(id=d_semester)
    students = Student.objects.filter(department=department_obj, semester=semester_obj)
    
    # Attendance on the specific date
    get_attendances = Attendance.objects.filter(department=department_obj, date=d_date, semester=semester_obj)
    
    # Calculate attendance percentages
    attendance_summary = []
    for student in students:
        total_classes = Attendance.objects.filter(department=department_obj, semester=semester_obj).count()
        present_count = Attendance.objects.filter(
            department=department_obj,
            semester=semester_obj,
            student_presents=student
        ).count()
        percentage = (present_count / total_classes * 100) if total_classes > 0 else 0
        attendance_summary.append({
            # 'student_id': student.id,
            'student_roll': student.roll,
            'student_name': student.name,
            'total_classes': total_classes,
            'present_count': present_count,
            'percentage': round(percentage, 2),
        })

    return attendance_summary


def calculate_month(m_department, m_semester, m_month):
    department_obj = Department.objects.get(id=m_department)
    semester_obj = Semester.objects.get(id=m_semester)
    students = Student.objects.filter(department=department_obj, semester=semester_obj)

    # Attendance records for the given month
    month_attendances = Attendance.objects.filter(department=department_obj, semester=semester_obj, month=m_month)

    # Calculate attendance summary for the month
    attendance_summary = []
    for student in students:
        total_classes = month_attendances.count()
        present_count = month_attendances.filter(student_presents=student).count()
        percentage = (present_count / total_classes * 100) if total_classes > 0 else 0
        attendance_summary.append({
            'student_roll': student.roll,
            'student_name': student.name,
            'total_classes': total_classes,
            'present_count': present_count,
            'percentage': round(percentage, 2),
        })

    return attendance_summary


def calculate_semester(s_department, s_semester, s_month_start, s_month_end):
    # Validate and parse input months
    try:
        start_date = datetime.strptime(s_month_start, "%B - %Y")
        end_date = datetime.strptime(s_month_end, "%B - %Y")
    except ValueError:
        return {"error": "Invalid date format. Please use 'Month - Year'."}

    # Validate date range
    if start_date > end_date:
        return {"error": "Start month cannot be greater than the end month."}

    # Determine the first and last day of the date range
    first_day = datetime(start_date.year, start_date.month, 1)
    last_day = datetime(end_date.year, end_date.month, monthrange(end_date.year, end_date.month)[1])

    # Get department and semester objects
    department_obj = Department.objects.get(id=s_department)
    semester_obj = Semester.objects.get(id=s_semester)
    students = Student.objects.filter(department=department_obj, semester=semester_obj)

    # Attendance records within the range
    semester_attendances = Attendance.objects.filter(
        department=department_obj,
        semester=semester_obj,
        date__gte=first_day,
        date__lte=last_day
    )

    # Debug: Log total attendance records
    print(f"Total attendance records found: {semester_attendances.count()}")

    # Calculate attendance summary
    attendance_summary = []
    for student in students:
        total_classes = semester_attendances.count()
        present_count = semester_attendances.filter(student_presents=student).count()
        percentage = (present_count / total_classes * 100) if total_classes > 0 else 0

        attendance_summary.append({
            'student_roll': student.roll,
            'student_name': student.name,
            'total_classes': total_classes,
            'present_count': present_count,
            'percentage': round(percentage, 2),
        })

    return attendance_summary
