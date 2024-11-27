from django.shortcuts import render, redirect
from session.models import Session
from django.http import HttpResponseRedirect
from django.contrib import messages

# Create your views here.

# seassons
def sessions(req):
    context = {
        'page': 'Sessions',
        'sessions': Session.objects.all().order_by('name')
    }
    return render(req, 'sessions/session.html', context)

def add_sessions(req):
    context = {
        'page': 'Add Dessions'
    }
    if req.method == 'POST':
        name = req.POST.get('session')
        year = req.POST.get('session_start')

        session_obj = Session.objects.filter(name=name).first()
        if session_obj:
            messages.warning(req, f'Session already exists!')
            return HttpResponseRedirect(req.path_info)
        
        else:
            try:
                session_obj = Session.objects.create(
                    name=name,
                    starting_year = year
                )

                messages.success(req, 'Session added Successfully!')
                return redirect('sessions')
            
            except Exception as e:
                messages.warning(req, f'Error while createing Session {name}: {e}')

    return render(req, 'sessions/add_session.html', context)