from django.shortcuts import render

# Create your views here.

# home
def home(request):
    context = {
        'page': 'Dashboard'
    }
    return render(request, 'home/index.html', context)