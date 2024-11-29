from django.shortcuts import render, redirect
from semesters.models import Semester
from departments.models import Department
from probidhans.models import Probidhan
from .models import Subject
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect


# Subjects view
def subjects(req):

    # Context initialization
    context = {
        'page': 'Subjects',
        'semesters': Semester.objects.all().order_by('name'),
        'probidhans': Probidhan.objects.all().order_by('name'),
        'departments': Department.objects.all().order_by('name'),
    }

    selected_department = req.GET.get('department', '')
    selected_semester = req.GET.get('semester', '')
    selected_probidhan = req.GET.get('probidhan', '')

    subjects = None

    if selected_department and selected_probidhan and selected_semester:
        subjects = Subject.objects.filter(
            department__slug = selected_department,
            semester__slug = selected_semester,
            probidhan__slug = selected_probidhan,
        ).order_by('code')

    context.update({
        'selected_department': selected_department,
        'selected_semester': selected_semester,
        'selected_probidhan': selected_probidhan,
        'subjects': subjects,
    })

    

    return render(req, 'subjects/subjects.html', context)



def add_subjects(req):
    context = {
        'page': 'Add Subjects',
        'semesters': Semester.objects.all().order_by('name'),
        'probidhans': Probidhan.objects.all().order_by('name'),
        'departments': Department.objects.all().order_by('name'),
    }

    if req.method == 'POST':
        name = req.POST.get('name')
        code = req.POST.get('code')

        # Fetch related instances using IDs
        subject_semester_id = req.POST.get('subject_semester')
        subject_department_id = req.POST.get('subject_department')
        subject_probidhan_id = req.POST.get('subject_probidhan')

        subject_theory = req.POST.get('subject_theory')
        subject_practical = req.POST.get('subject_practical')
        subject_credit = req.POST.get('subject_credit')

        try:
            # Convert IDs to model instances
            subject_semester = Semester.objects.get(id=subject_semester_id)
            subject_department = Department.objects.get(id=subject_department_id)
            subject_probidhan = Probidhan.objects.get(id=subject_probidhan_id) if subject_probidhan_id else None

            # Check if the subject already exists
            subject_obj = Subject.objects.filter(
                name=name,
                code=code,
                semester=subject_semester,
                department=subject_department,
                probidhan=subject_probidhan,
                theory=subject_theory,
                practical=subject_practical,
                credit=subject_credit,
            ).first()

            if subject_obj:
                messages.warning(req, 'Subject already exists!')
                return HttpResponseRedirect(req.path_info)
            else:
                # Create a new subject
                subject_obj = Subject.objects.create(
                    name=name,
                    code=code,
                    semester=subject_semester,
                    department=subject_department,
                    probidhan=subject_probidhan,
                    theory=subject_theory,
                    practical=subject_practical,
                    credit=subject_credit,
                )

                messages.success(req, 'Subject added successfully!')
                return redirect('subjects')

        except Semester.DoesNotExist:
            messages.warning(req, 'Invalid semester selected!')
        except Department.DoesNotExist:
            messages.warning(req, 'Invalid department selected!')
        except Probidhan.DoesNotExist:
            messages.warning(req, 'Invalid probidhan selected!')
        except Exception as e:
            messages.warning(req, f'Error while creating {name}: {e}')
            return HttpResponseRedirect(req.path_info)

    return render(req, 'subjects/add_subjects.html', context)
