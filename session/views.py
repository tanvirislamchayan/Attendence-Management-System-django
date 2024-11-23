from django.shortcuts import render

# Create your views here.

# seassons
def sessions(req):
    context = {
        'page': 'Sessions'
    }
    return render(req, 'sessions/session.html', context)

def add_sessions(req):
    context = {
        'page': 'Add Dessions'
    }
    return render(req, 'sessions/add_session.html', context)