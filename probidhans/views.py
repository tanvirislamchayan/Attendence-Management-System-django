from django.shortcuts import render

# Create your views here.

# probidhans
def probidhans(req):
    context = {
        'page': 'Probidhans'
    }
    return render(req, 'probidhan/probidhan.html', context)



def add_probidhans(req):
    context = {
        'page': 'Add Probidhans'
    }
    return render(req, 'probidhan/add_probidhan.html', context)