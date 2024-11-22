from django.shortcuts import render

# Create your views here.

# departments
def departments(request):
    context = {
        'page': 'Deprtments'
    }
    return render(request, 'departments/department.html', context)


def add_departments(req):
    context = {
        'page': 'Add Departments'
    }

    return render(req, 'departments/add_departments.html', context)