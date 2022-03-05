from django.shortcuts import render , redirect , get_object_or_404 , get_list_or_404
from School.Requirments.models import *
from .models import *
from School.Teacher.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from App.Authentication.user_handeling import unauthenticated_user, allowed_users, admin_only
from datetime import timedelta
import datetime


@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Admin','Teacher'])
def ManageDateSelectView(request):
    user = request.user.groups.values('name')
    if request.method == 'POST':
        Date = request.POST.get('date')
        return redirect('school:class_select',Date)
    context = {
        'user':user ,
    }
    return render(request , 'Select/date.html',context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Admin','Teacher'])
def ManageClassSelectView(request,date):
    user = request.user.groups.values('name')
    curr_teacher = ''
    if request.user.is_authenticated:
        for i in user:
            if str(i.get('name')) == 'Teacher':
                teacher = request.user
                for i in TeacherClass.objects.all():
                    if str(i.teacher.pk) == str(teacher.pk):
                        curr_teacher = i
                return redirect('school:subject_select',date,curr_teacher.clas.pk)
    FDate = date
    FClass = Classes.objects.all()
    context = {
        'user':user ,
        'date' : FDate,
        'class' : FClass,
    }
    return render(request , 'Select/class.html' , context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Admin','Teacher'])
def ManageSubjectSelectView(request,date,Ccode):
    user = request.user.groups.values('name')
    list_ = []
    FClassSubjects = []
    if request.user.is_authenticated:
        for i in user:
            if str(i.get('name')) == 'Teacher':
                for v in Content.objects.all():
                    for k in TeacherClass.objects.all():
                        sess_date = get_object_or_404(Session , pk = k.session.pk).session_start_date
                        d1 = datetime.datetime.strptime(str(sess_date - timedelta(days=1)), "%Y-%m-%d")
                        d2 = datetime.datetime.strptime(date, "%Y-%m-%d")
                        day = abs((d2 - d1).days)
                        if str(v.day) == str(day) and str(v.class_name.pk) == str(Ccode):
                            if str(v.therefor) == 'O':
                                list_.append(v)
                context = {
                    'list':list_,
                    'user':user ,
                }
                return render (request,'Lists/content.html',context)
    FDate = date
    FClass = get_object_or_404(Classes, code = Ccode)
    for i in ClassSubjects.objects.all():
        if str(i.class_name.pk) == str(Ccode):
            FClassSubjects.append(i)
    context = {
        'user':user ,
        'date' : FDate,
        'class' : FClass,
        'class_subjects' : FClassSubjects,
    }
    return render(request , 'Select/subject.html' , context)
    
def ManageSessionSelectView(request,date,Ccode,subject):
    user = request.user.groups.values('name')
    session = Session.objects.all()
    context = {
        'user':user ,
        'date' : date,
        'class' : Ccode,
        'class_subjects' : subject,
        'session' : session ,
    }
    return render(request , 'Select/session.html' , context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Admin','Teacher'])
def ManageContentSelectView(request,date,Ccode,subject,session):
    user = request.user.groups.values('name')
    class_ = get_object_or_404(Classes , pk = Ccode)
    subject = get_object_or_404(Subjects , subject_name = subject)
    session = get_object_or_404(Session , pk = session)
    cont = []
    for i in Content.objects.all():
        if str(i.subject.pk) == str(subject.pk):
            if str(i.class_name.pk) == str(class_.pk):
                if str(str(session.session_start_date + timedelta(days=i.day-1))) == str(date):
                    cont.append(i)
    context = {'user':user ,'content' : cont,}
    return render(request , 'Select/content_select.html' , context)

def ManageContentView(request, code):
    Contents = get_object_or_404(Content,code = code)
    user = request.user.groups.values('name')
    videos = []
    for i in Videos.objects.all():
        if str(i.content.pk) == str(Contents.pk):
            videos.append(i)
    images = []
    for i in Images.objects.all():
        if str(i.content.pk) == str(Contents.pk):
            images.append(i)
    context = {
        'user': user ,
        'content' : Contents ,
        'videos' : videos ,
        'images' : images ,
    }
    return render(request , 'Select/content.html' , context)