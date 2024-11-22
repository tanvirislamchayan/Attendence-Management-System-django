from django.shortcuts import render

# Create your views here.

# groups 
def groups(req):
    context = {
        'page': 'Groups/Shifts'
    }

    return render(req, 'groups/group.html', context)

def add_groups(req):
    context = {
        'page': 'Add Groups/Shifts'
    }

    return render(req, 'groups/add_group.html', context)