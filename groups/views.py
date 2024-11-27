from django.shortcuts import render, redirect
from .models import Group
from django.http import HttpResponseRedirect
from django.contrib import messages

# Create your views here.

# groups 
def groups(req):
    context = {
        'page': 'Groups/Shifts',
        'groups': Group.objects.all().order_by('name')
    }

    return render(req, 'groups/group.html', context)

def add_groups(req):
    context = {
        'page': 'Add Groups/Shifts'
    }

    if req.method == 'POST':
        name = req.POST.get('shift')

        group_obj = Group.objects.filter(name=name)
        if group_obj:
            messages.warning(req, f'Group/shift already exists!')
            return HttpResponseRedirect(req.path_info)
        else:
            try:
                group_obj = Group.objects.create(
                    name=name
                )
                messages.success(req, 'Group/Shift added successfully!')
                return redirect('groups')
            except Exception as e:
                messages.warning(req, f'Error while creating {name}: {e}')
                return HttpResponseRedirect(req.path_info)

    return render(req, 'groups/add_group.html', context)