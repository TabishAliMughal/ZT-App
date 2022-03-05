from django.shortcuts import render , redirect , get_object_or_404 , get_list_or_404
from School.Requirments.models import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from Authentication.user_handeling import unauthenticated_user, allowed_users, admin_only
from Authentication.views import *
from School.Teacher.models import *
from .forms import *
import datetime
from datetime import timedelta

def ManageMainView(request):
    user = request.user.groups.values('name')
    v = '1'
    tea = []
    for i in TeacherClass.objects.all():
        loc = []
        map = i.location
        for m in map:
            loc.append(m)
        tea.append({'num':int(v),'teacher':i,'lat':loc[1],'lon':loc[0]})
        v = int(v) + 1
    context = {
        'locator':tea ,
        'user':user ,
    }
    for i in user:
        if str(i.get('name')) == 'Teacher':
            return redirect('school_teacher:teacher_profile')
        elif str(i.get('name')) == 'Admin':
            return redirect('school_admin:profiles')
        elif str(i.get('name')) == 'Checker':
            return redirect('school_checker:checker_profile')
        elif str(i.get('name')) == 'School':
            return redirect('school_reg_school:school_profile')
        elif str(i.get('name')) == 'Parent':
            return redirect('school_parents:parent_profile')
        elif str(i.get('name')) == 'Student':
            return redirect('school_student:student_profile',request.user.pk)
        elif str(i.get('name')) == 'Individuals':
            return redirect('school_individuals:indivisual_profile')
        else:
            pass
        #     logoutUser(SelectView)
    return render(request , 'MainContent.html',context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Admin'])
def ManageSelectToAddView(request):
    user = request.user.groups.values('name')
    context = {
        'user':user ,
    }
    return render(request , 'Forms/All.html' , context)

def ManageAllView(request):
    user = request.user.groups.values('name')
    context = {
        'user':user ,
    }
    return render(request , 'All.html' , context)

def ManageDemoView(request):
    user = request.user.groups.values('name')
    f = []
    for i in range(1,8):
        f.append(i)
    k = []
    for i in range(8,15):
        k.append(i)
    context = {
        'date1': f ,
        'date2': k ,
        'user': user ,
    }
    return render(request , 'Demo.html' , context)

def ManageDemoListView(request , demodate = None , filday = None):
    user = request.user.groups.values('name')
    if filday:
        day = filday
    else:
        day = int(demodate)
    classes = Classes.objects.all()
    context = {
        'user' : user ,
        'day' : day ,
        'classes' : classes ,
    }
    return render(request , 'Select/DemoClasses.html' , context)


def ManageDemoContentView(request , day , clas):
    user = request.user.groups.values('name')
    content = []
    k = int('0')
    for i in Content.objects.all():
        if str(clas) == str(i.class_name.pk) and str(day) == str(i.day):
            k = k + 1
            content.append({
                'period' : k ,
                'pk': i.pk ,
                'class_name' : i.class_name ,
                'subject' : i.subject ,
                'module' : i.module ,
            })
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    try:
        visit = get_object_or_404(Visits,page = 'DemoList')
    except:
        visit = ''
    if visit:
        if str(visit.date) != str(datetime.date.today()):
            form = VisitsForm({
                'page' : 'DemoList' ,
                'visits' : num_visits ,
                'date' : datetime.date.today() ,
            } or None , instance = visit)
            form.save()
        else:
            form = VisitsForm({
                'page' : 'DemoList' ,
                'visits' : num_visits ,
                'date' : datetime.date.today() ,
            } or None , instance = visit)
            form.save()
    context = {
        'date' : day ,
        'content' : content,
        'user': user ,
        'clas' : get_object_or_404(Classes , pk = clas) ,
    }
    return render(request , 'Lists/DemoContent.html' , context)
