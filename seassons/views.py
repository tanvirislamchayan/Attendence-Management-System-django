from django.shortcuts import render

# Create your views here.

# seassons
def seassons(req):
    context = {
        'page': 'Seassons'
    }
    return render(req, 'seassons/seasson.html', context)

def add_seassons(req):
    context = {
        'page': 'Seassons'
    }
    return render(req, 'seassons/add_seasson.html', context)