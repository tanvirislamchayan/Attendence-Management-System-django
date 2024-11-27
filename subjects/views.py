from django.shortcuts import render, redirect
from semesters.models import Semester
from departments.models import Department
from probidhans.models import Probidhan
from .models import Subject
from django.urls import reverse

# Global variables to hold state
SUBJECTS = None
REQ_SEM = None

# Subjects view
def subjects(req):
    global SUBJECTS, REQ_SEM
    print(f'req_sem {REQ_SEM}')

    # Context initialization
    context = {
        'page': 'Subjects',
        'semesters': Semester.objects.all().order_by('name'),
        'probidhans': Probidhan.objects.all().order_by('name'),
        'departments': Department.objects.all().order_by('name'),
        'subjects': None,
        'rec_sem': None,
    }

    if req.method == 'POST':
        # Fetch form data from POST request
        semester = req.POST.get('semester')
        department = req.POST.get('department')
        probidhan = req.POST.get('probidhan')

        if semester and department and probidhan:
            REQ_SEM = Semester.objects.get(id=semester)
            # Store filter data in the session and redirect
            req.session['subjects_filter'] = {
                'semester': semester,
                'department': department,
                'probidhan': probidhan
            }
            return redirect(reverse('subjects'))  # Replace 'subjects' with the name of your URL pattern for this view.

    # Handle filter data after redirect
    filters = req.session.pop('subjects_filter', None)
    if filters:
        # Apply filters and update global variables
        SUBJECTS = Subject.objects.filter(
            semester=filters['semester'],
            department=filters['department'],
            probidhan=filters['probidhan']
        )
        context['subjects'] = SUBJECTS
        context['rec_sem'] = REQ_SEM
    else:
        # Use cached values for subjects and semester
        context['subjects'] = SUBJECTS
        context['rec_sem'] = REQ_SEM
    print(context)
    

    return render(req, 'subjects/subjects.html', context)



def add_subjects(req):
    context = {
        'page': 'Add Subjects'
    }

    return render(req, 'subjects/add_subjects.html', context)