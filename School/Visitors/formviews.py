from django.shortcuts import render , redirect
from . models import *
from .forms import *

def ManageTeacherVisitCreateView(request):
    if request.method == 'POST':
        form = ManageTeacherVisitForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('main')
    else:
        form = ManageTeacherVisitForm()
        context = {
            'form': form ,
        }
        return render(request , 'Visits/Teacher/Create.html',context)

def ManageSchoolVisitCreateView(request):
    if request.method == 'POST':
        form = ManageSchoolVisitForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('main')
    else:
        form = ManageSchoolVisitForm()
        context = {
            'form': form ,
        }
        return render(request , 'Visits/School/Create.html',context)

def ManageParentVisitCreateView(request):
    if request.method == 'POST':
        form = ManageParentVisitForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('main')
    else:
        form = ManageParentVisitForm()
        context = {
            'form': form ,
        }
        return render(request , 'Visits/Parent/Create.html',context)
