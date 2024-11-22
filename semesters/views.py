from django.shortcuts import render

# Create your views here.

# semesters
def semesters(req):
    context = {
        'page': 'Semesters'
    }
    return render(req, 'semesters/semester.html', context)

def add_semesters(req):
    context = {
        'page': 'Add Semesters'
    }
    return render(req, 'semesters/add_semester.html', context)