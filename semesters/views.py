from django.shortcuts import render, redirect
from .models import Semester
from django.contrib import messages
from django.http import HttpResponseRedirect

# Create your views here.

# semesters
def semesters(req):
    context = {
        'page': 'Semesters',
        'semesters': Semester.objects.all().order_by('name')
    }
    return render(req, 'semesters/semester.html', context)

def add_semesters(req):
    context = {
        'page': 'Add Semesters'
    }

    if req.method == 'POST':
        name = req.POST.get('semester')

        semester_obj = Semester.objects.filter(name=name).first()
        if semester_obj:
            messages.warning(req, 'The Semester already exists!')
            return HttpResponseRedirect(req.path_info)
        else:
            try:
                semester_obj = Semester.objects.create(
                    name = name
                )

                messages.success(req, 'Semester added Successfully!')
                return redirect('semesters')
            except Exception as e:
                messages.warning(req, f'Error while creating Semester {name}: {e}')
                return HttpResponseRedirect(req.path_info)

    return render(req, 'semesters/add_semester.html', context)