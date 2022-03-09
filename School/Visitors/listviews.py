from django.shortcuts import render
from . models import *

def ManageTeacherVisitListView(request):
    Teachers = TeacherVisit.objects.all()
    context = {
        'Teachers' : Teachers ,
    }
    return render(request , 'Visits/Teacher/list.html' , context)

def ManageSchoolVisitListView(request):
    Schools = SchoolVisit.objects.all()
    context = {
        'Schools' : Schools ,
    }
    return render(request , 'Visits/School/list.html' , context)

def ManageParentVisitListView(request):
    Parents = ParentVisit.objects.all()
    context = {
        'Parents' : Parents ,
    }
    return render(request , 'Visits/Parent/list.html' , context)

