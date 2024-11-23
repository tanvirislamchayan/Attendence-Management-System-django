from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Teacher, User, Designation
from departments.models import Department
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.core.files.storage import default_storage

# Create your views here.

# authors
def authors(request):
    context = {
        'page': 'Authors'
    }

    authors = Teacher.objects.filter(is_author=True, is_active=True, is_teacher=True)

    context.update({
        'authors': authors
    })

    return render(request, 'author/author.html', context)




def add_authors(request):
    context = {
        'page': 'Add Author',
        'designations': Designation.objects.all(),
        'departments': Department.objects.all()
    }

    if request.method == 'POST':
        name = request.POST.get('name')
        phone_no = request.POST.get('phone_no')
        email = request.POST.get('email')
        password = request.POST.get('pass')
        re_pass = request.POST.get('re_pass')
        designation = request.POST.get('designation')
        department = request.POST.get('department')
        details = request.POST.get('details')
        is_author = request.POST.get('is_author') == 'on'
        is_teacher = request.POST.get('is_teacher') == 'on'
        image = request.FILES.get('image')

        if password != re_pass:
            messages.error(request, 'Passwords do not match.')
            return redirect(request.path_info)

        if User.objects.filter(username=email).exists():
            messages.warning(request, 'A user with this email already exists.')
            return redirect(request.path_info)

        try:
            user_obj = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=name
            )
        except Exception as e:
            messages.warning(request, f"Error creating user: {e}")
            return redirect(request.path_info)

        try:
            teacher = Teacher(
                user=user_obj,
                mobile_number=phone_no,
                designation_id=designation,
                department_id=department,
                details=details,
                is_author=is_author,
                is_teacher=is_teacher,
                is_active=True
            )

            if image:
                teacher.image = image

            teacher.save()

            messages.success(request, 'Author added successfully.')
            return redirect('authors')  # Redirect to authors page

        except Exception as e:
            user_obj.delete()
            messages.error(request, f"Error creating author: {e}")
            return redirect(request.path_info)

    return render(request, 'author/add_author.html', context)

    
def teachers(request):
    context = {
        'page': 'Teachers',
        'departments': Department.objects.filter(teachers__isnull=False).distinct()  # Fetch departments with teachers
    }

    # Fetch active teachers who are marked as teachers and authors
    teachers = Teacher.objects.filter(is_teacher=True, is_active=True)

    # Process short forms dynamically and attach them to the teacher
    for teacher in teachers:
        # Generate short designation if designation exists
        if teacher.designation and teacher.designation.name:
            short_designation = ''.join(
                word[0].upper() for word in teacher.designation.name.split() 
                if word.lower() not in ['and', 'for', 'or']
            )
        else:
            short_designation = None

        # Generate short department if department exists
        if teacher.department and teacher.department.name:
            short_department = ''.join(
                word[0].upper() for word in teacher.department.name.split() 
                if word.lower() not in ['and', 'for', 'or']
            )
        else:
            short_department = None

        # Attach the short forms to the teacher object dynamically
        teacher.short_designation = short_designation
        teacher.short_department = short_department

    # Update context to include teachers
    context.update({
        'teachers': teachers
    })

    return render(request, 'teacher/teacher.html', context)


def add_teachers(request):
    context = {
        'page': 'Add Teacher'
    }
    return render(request, 'teacher/add_teacher.html', context)