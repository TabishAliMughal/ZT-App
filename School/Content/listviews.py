from django.shortcuts import render , redirect , get_object_or_404 , get_list_or_404
from School.Requirments.models import *
from .models import *
from School.Exam.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group , User
from Authentication.user_handeling import unauthenticated_user, allowed_users, admin_only
import datetime
from datetime import timedelta


@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Admin'])
def ManageClassListView(request):
    list_ = Classes.objects.all()
    user = request.user.groups.values('name')
    context = {
        'list':list_,
        'user':user ,
    }
    return render (request,'Lists/classes.html',context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Admin','DataHandler'])
def ManageContentListView(request):
    user = request.user.groups.values('name')
    session = get_object_or_404(Session , session_number = '1')
    if request.method == 'POST':
        list_ = []
        if request.POST.get('day'):
            for i in Content.objects.all():
                ses_day = str(get_object_or_404(Session , session_number = '1').session_start_date)
                d1 = datetime.datetime.strptime(str(ses_day), "%Y-%m-%d").date()
                d2 = datetime.datetime.strptime(str(request.POST.get('date')), "%Y-%m-%d").date()
                day = str((d2 - d1))[:-14]
                if str(day - 1) == str(i.day):
                    if str(i.class_name.pk) == str(request.POST.get('class')):
                        list_.append(i)
            return redirect('school:content_by_date',request.POST.get('day'))
        if request.POST.get('class'):
            for i in Content.objects.all():
                if str(i.class_name.pk) == str(request.POST.get('class')):
                    if str(request.POST.get('subject')) == str(i.subject.pk):
                        list_.append(i)
        classes = Classes.objects.all()
        subjects = Subjects.objects.all()
        context = {
            'list':list_,
            'user':user ,
            'classes':classes ,
            'subjects':subjects ,
        }
        return render (request,'Lists/content.html',context)
    else:
        cont = Content.objects.all().order_by('-code')
        list_ = []
        k = int('0')
        for i in cont:
            if k <= 4 :
                list_.append(i)
                k = k + 1
        classes = Classes.objects.all()
        subjects = Subjects.objects.all()
        context = {
            'list':list_,
            'user':user ,
            'classes':classes ,
            'subjects':subjects ,
        }
        return render (request,'Lists/content.html',context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Admin'])
def ManageSubjectListView(request):
    list_ = Subjects.objects.all()
    user = request.user.groups.values('name')
    context = {
        'list':list_,
        'user':user ,
    }
    return render (request,'Lists/subjects.html',context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Admin'])
def ManageModuleListView(request):
    list_ = Module.objects.all()
    user = request.user.groups.values('name')
    context = {
        'list':list_,
        'user':user ,
    }
    return render (request,'Lists/module.html',context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Admin'])
def ManageClassSubjectsListView(request):
    list_ = ClassSubjects.objects.all()
    user = request.user.groups.values('name')
    context = {
        'list':list_,
        'user':user ,
    }
    return render (request,'Lists/classsubjects.html',context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Admin'])
def ManageExamListView(request):
    list_ = ExamStatus.objects.all()
    user = request.user.groups.values('name')
    context = {
        'list':list_,
        'user':user ,
    }
    return render (request,'Lists/exam.html',context)
