from django.shortcuts import render

# Create your views here.

# authors
def authors(request):
    context = {
        'page': 'Authors'
    }
    return render(request, 'author/author.html', context)

def add_authors(request):
    context = {
        'page': 'Add Author'
    }
    return render(request, 'author/add_author.html', context)
    

# teachers
def teachers(request):
    context = {
        'page': 'Teachers'
    }

    return render(request, 'teacher/teacher.html', context)


def add_teachers(request):
    context = {
        'page': 'Add Teacher'
    }
    return render(request, 'teacher/add_teacher.html', context)