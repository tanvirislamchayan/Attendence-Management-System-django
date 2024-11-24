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
            messages.warning(request, 'Passwords do not match.')
            return redirect(request.path_info)

        if User.objects.filter(username=email).exists():
            messages.warning(request, 'A user with this email already exists.')
            return redirect(request.path_info)

        try:
            user_obj = User.objects.create_user(
                username=email,
                email=email,
                first_name=name
            )
            user_obj.set_password(password)
            user_obj.save()
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
            messages.warning(request, f"Error creating author: {e}")
            return redirect(request.path_info)

    return render(request, 'author/add_author.html', context)

def teachers(request):
    context = {
        'page': 'Teachers',
        'departments': Department.objects.filter(
            teachers__is_teacher=True, teachers__is_active=True
        ).distinct()  # Fetch departments with at least one active teacher
    }

    # Attach filtered teachers to departments
    for department in context['departments']:
        department.filtered_teachers = department.teachers.filter(is_teacher=True, is_active=True)

    return render(request, 'teacher/teacher.html', context)


def add_teachers(request):
    context = {
        'page': 'Add Teacher',
        'designations': Designation.objects.all(),
        'departments': Department.objects.all(),
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
        image = request.FILES.get('image')
        is_author = request.POST.get('is_author') == 'on'
        is_teacher = request.POST.get('is_teacher') == 'on'

        # Validate password match
        if password != re_pass:
            messages.warning(request, 'Passwords do not match.')
            return redirect(request.path_info)

        # Check for duplicate email
        if User.objects.filter(username=email).exists():
            messages.warning(request, 'A user with this email already exists.')
            return redirect(request.path_info)

        try:
            # Create user
            user_obj = User.objects.create_user(
                username=email,
                email=email,
                first_name=name
            )
        except Exception as e:
            messages.warning(request, f"Error creating user: {e}")
            return redirect(request.path_info)

        try:
            # Create teacher instance
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

            # Save image if provided
            if image:
                teacher.image = image

            teacher.save()

            messages.success(request, 'Teacher added successfully.')
            return redirect('teachers')  # Redirect to teachers page
        except Exception as e:
            # Rollback user creation if teacher creation fails
            user_obj.delete()
            messages.warning(request, f"Error creating teacher: {e}")
            return redirect(request.path_info)

    return render(request, 'teacher/add_teacher.html', context)
