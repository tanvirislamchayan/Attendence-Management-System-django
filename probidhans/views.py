from django.shortcuts import render, redirect
from .models import Probidhan
from django.contrib import messages
from django.http import HttpResponseRedirect

# probidhans
def probidhans(req):
    if not req.user.is_authenticated:
        messages.warning(req, 'Login First!!')
        return redirect('user_login')

    context = {
        'page': 'Probidhans',
        'probidhans': Probidhan.objects.all().order_by('name')
    }
    return render(req, 'probidhan/probidhan.html', context)


# add_probidhans
def add_probidhans(req):
    context = {
        'page': 'Add Probidhans'
    }
    if req.method == 'POST':
        name = req.POST.get('probidhan')
        year = req.POST.get('year')

        # Validate that both fields are provided and are integers
        if not name or not name.isdigit():
            messages.warning(req, "Probidhan must be a valid number.")
            return HttpResponseRedirect(req.path_info)
        if not year or not year.isdigit():
            messages.warning(req, "Year must be a valid number.")
            return HttpResponseRedirect(req.path_info)

        name = int(name)  # Convert validated name to integer
        year = int(year)  # Convert validated year to integer

        # Check if a Probidhan with the same name already exists
        pro_obj = Probidhan.objects.filter(name=name)
        if pro_obj.exists():
            messages.warning(req, "The Probidhan already exists.")
            return HttpResponseRedirect(req.path_info)
        else:
            try:
                # Create a new Probidhan
                Probidhan.objects.create(
                    name=name,
                    starting_year=year
                )
                messages.success(req, 'Probidhan created successfully.')
                return redirect('probidhans')
            except Exception as e:
                # Handle any exceptions during object creation
                messages.warning(req, f'Error while creating Probidhan: {e}')
                return redirect(req.path_info)

    return render(req, 'probidhan/add_probidhan.html', context)