from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Department


# Create your views here.

# departments
def departments(request):
    context = {
        'page': 'Deprtments',
        'departments': Department.objects.all()
    }

    return render(request, 'departments/department.html', context)



def add_departments(req):
    context = {
        'page': 'Add Departments'
    }

    if req.method == 'POST':
        name = req.POST.get('name')
        details = req.POST.get('details')
        image = req.FILES.get('image')  # Use req.FILES for file inputs

        if not name:
            messages.error(req, 'Department name is required.')
            return redirect(req.path_info)
        
        # Check if a department with the same name already exists
        if Department.objects.filter(name__iexact=name).exists():
            messages.warning(req, 'A department with this name already exists.')
            return redirect(req.path_info)

        try:
            # Create the department object
            department_obj = Department(
                name=name,
                details=details,
                image=image  # This is optional, so it can be None
            )
            department_obj.save()

            messages.success(req, 'Department added successfully.')
            return redirect('departments')  # Redirect to the departments page

        except Exception as e:
            # Handle errors gracefully
            messages.error(req, f'Error while adding department: {e}')
            return redirect(req.path_info)

    return render(req, 'departments/add_departments.html', context)

