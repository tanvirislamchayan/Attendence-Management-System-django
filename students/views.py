from django.shortcuts import render

# Create your views here.
# students
def students(req):
    context = {
        'page': 'Students'
    }

    return render(req, 'students/students.html', context)

def add_students(req):
    context = {
        'page': 'Add Students'
    }

    return render(req, 'students/add_students.html', context)