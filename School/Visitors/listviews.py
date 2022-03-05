from django.shortcuts import render
from . models import *

def ManageTeacherVisitListView(request):
    user = request.user.groups.values('name')
    Teachers = TeacherVisit.objects.all()
    context = {
        'Teachers' : Teachers ,
        'user' : user ,
    }
    return render(request , 'Visits/Teacher/list.html' , context)

def ManageSchoolVisitListView(request):
    user = request.user.groups.values('name')
    Schools = SchoolVisit.objects.all()
    context = {
        'Schools' : Schools ,
        'user' : user ,
    }
    return render(request , 'Visits/School/list.html' , context)

def ManageParentVisitListView(request):
    user = request.user.groups.values('name')
    Parents = ParentVisit.objects.all()
    context = {
        'Parents' : Parents ,
        'user' : user ,
    }
    return render(request , 'Visits/Parent/list.html' , context)

