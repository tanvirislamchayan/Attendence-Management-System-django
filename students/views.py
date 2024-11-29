from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from departments.models import Department
from semesters.models import Semester
from probidhans.models import Probidhan
from groups.models import Group
from session.models import Session
from .models import Student
from .resources import StudentResource
from tablib import Dataset


# Create your views here.
# students
def students(request):
    context = {
        'page': 'Students',
        'departments': Department.objects.all().order_by('name'),
        'semesters': Semester.objects.all().order_by('name'),
        'probidhans': Probidhan.objects.all().order_by('name'),
    }

    selected_semester = request.GET.get('semester', '')
    selected_department = request.GET.get('department', '')
    selected_probidhan = request.GET.get('probidhan', '')

    students = None
    if selected_department and selected_probidhan and selected_semester:
        students = Student.objects.filter(
            department__slug=selected_department,
            semester__slug=selected_semester,
            probidhan__slug=selected_probidhan,
        ).order_by('roll')

    context.update({
        'selected_semester': selected_semester,
        'selected_department': selected_department,
        'selected_probidhan': selected_probidhan,
        'students': students
    })
        

    return render(request, 'students/students.html', context)

def add_students(req):
    context = {
        'page': 'Add Students',
        'departments': Department.objects.all().order_by('name'),
        'semesters': Semester.objects.all().order_by('name'),
        'probidhans': Probidhan.objects.all().order_by('name'),
        'groups': Group.objects.all().order_by('name'),
        'sessions': Session.objects.all().order_by('name'),
    }

    return render(req, 'students/add_students.html', context)

# add by form
def add_students_by_form(request):
    if request.method == 'POST':
        std_name = request.POST.get('std_name')
        std_code = request.POST.get('std_code')
        std_roll = request.POST.get('std_roll')
        std_department = request.POST.get('std_department')
        std_seasson = request.POST.get('std_seasson')
        std_shift = request.POST.get('std_shift')
        std_semester = request.POST.get('std_semester')
        std_probidhan = request.POST.get('std_probidhan')

        student_obj = Student.objects.filter(roll=std_roll).first()

        if student_obj:
            messages.warning(request, 'Student already exists')
            return HttpResponseRedirect(request.path_info)
        
        else:
            try:
                dep_obj = Department.objects.get(id=std_department)
                ses_obj = Session.objects.get(id=std_seasson)
                grp_obj = Group.objects.get(id=std_shift)
                sem_obj = Semester.objects.get(id=std_semester)
                pro_obj = Probidhan.objects.get(id=std_probidhan)

                student_obj = Student.objects.create(
                    name = std_name,
                    roll = std_roll,
                    department = dep_obj,
                    semester = sem_obj,
                    session = ses_obj,
                    probidhan = pro_obj,
                    group = grp_obj
                )
                messages.success(request, f'Student named {std_name} added successfully')
                return redirect('students')

            except Exception as e:
               messages.warning(request, f'Error while creating <span style="color:red;"> {std_name} </span>: {e}')


# xlsx
# def add_by_xlsx(request):
#     if request.method == 'POST':
#         student_resource = StudentResource()
#         dataset = Dataset()
#         students_xlsx = request.FILES['std_excel']

#         if not students_xlsx.name.endswith('xlsx'):
#             messages.warning(request, 'Please import a file with "xlsx" extenstion !!')
#             return HttpResponseRedirect(request.path_info)
        
#         std_data = dataset.load(students_xlsx.read(),format='xlsx')
#         print(std_data)
#     return redirect('add_students')


def add_by_xlsx(request):
    if request.method == 'POST':
        student_resource = StudentResource()
        dataset = Dataset()
        students_xlsx = request.FILES['std_excel']

        # Check if the file is an xlsx
        if not students_xlsx.name.endswith('xlsx'):
            messages.warning(request, 'Please import a file with "xlsx" extension !!')
            return HttpResponseRedirect(request.path_info)
        
        # Load the dataset
        std_data = dataset.load(students_xlsx.read(), format='xlsx')
        print(std_data)  # For debugging purposes

        std_exist = []
        std_created = []
        # Iterate through each row in the dataset
        for row in std_data.dict:
            try:
                # Get or create related foreign key objects
                department, _ = Department.objects.get_or_create(name=row['Department'])
                semester, _ = Semester.objects.get_or_create(name=row['Semester'])
                session, _ = Session.objects.get_or_create(name=row['Session'])
                probidhan, _ = Probidhan.objects.get_or_create(name=row['Probidhan'])
                group, _ = Group.objects.get_or_create(name=row['Group'])

                # Create the Student object, ensuring roll number is unique
                student, created = Student.objects.get_or_create(
                    roll=row['Roll'],
                    defaults={
                        'name': row['Name'],
                        'department': department,
                        'semester': semester,
                        'session': session,
                        'probidhan': probidhan,
                        'group': group
                    }
                )

                if created:
                    std_created.append(str(student.roll))  # Convert to string
                    print(f"Student {student.name} created successfully.")
                else:
                    std_exist.append(str(student.roll))  # Convert to string
                    print(f"Student with roll {student.roll} already exists.")

            except Exception as e:
                print(f"Error processing row {row}: {e}")
                messages.error(request, f"Error processing row {row['Roll']}: {e}")

        if std_created:
            messages.success(request, f"status: \n Student/s with roll/s {', '.join(std_created)} are created successfully.")

        if std_exist:
            messages.warning(request, f"status: \n Student/s with roll/s {', '.join(std_exist)} already exist.")

    return redirect('add_students')
