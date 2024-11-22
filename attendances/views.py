from django.shortcuts import render

# Create your views here.

# attendance
def attendance(req):
    context = {
        'page': 'Attendance'
    }
    return render(req, 'attendance/attendance.html', context)

def calculate_attendance(req):
    context = {
        'page': 'Attendance Calculation'
    }
    return render(req, 'attendance/atd_calculation.html', context)