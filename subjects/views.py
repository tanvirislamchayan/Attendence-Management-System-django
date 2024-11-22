from django.shortcuts import render

# Create your views here.

# subjects
def subjects(req):
    context = {
        'page': 'Subjects'
    }

    return render(req, 'subjects/subjects.html', context)


def add_subjects(req):
    context = {
        'page': 'Add Subjects'
    }

    return render(req, 'subjects/add_subjects.html', context)