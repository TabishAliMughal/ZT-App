from django.http import request
from django.shortcuts import render , redirect , get_object_or_404 , get_list_or_404 , HttpResponse
from .models import *
from .forms import *
from Authentication.forms import *
import random
from django.contrib.auth.models import User , Group
from School.Content.models import *
import datetime
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group , User
from Authentication.user_handeling import unauthenticated_user, allowed_users, admin_only
from School.Exam.models import *
from django.template import loader



@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Individuals'])
def ManageIndivisualProfileView(request , pk = None):
    user = request.user.groups.values('name')
    individual = ""
    for i in user:
        if str(i.get('name')) == 'Individuals':
            curuser = request.user
    for i in Indivisuals.objects.all():
        if str(i.user) == str(curuser.pk):
            individual = i
    content = []
    prev_content = []
    v = int('1')
    d = int('1')
    for i in Content.objects.all():
        if str(i.class_name.pk) == str(individual.clas.pk):
            if str(str(individual.start_date + timedelta(days=i.day-1))) == str(datetime.date.today()):
                content.append({'content':i,'period':v})
                v = v + 1
            if str(str(individual.start_date + timedelta(days=i.day))) == str(datetime.date.today()):
                prev_content.append({'content':i,'period':d})
                d = d + 1
    exam = []
    for i in ExamStatus.objects.all():
        if str(individual.clas.code) == str(i.class_name.pk):
            if str(individual.session.pk) == str(i.session.pk):
                if str(i.status) == 'True':
                    exam.append({'exam':i,'period':v})
                    v = v + 1
    if pk:
        content = []
        for i in Content.objects.all():
            if str(i.pk) == str(pk):
                videos = []
                images = []
                for vid in Videos.objects.all():
                    if str(i.pk) == str(vid.content.pk):
                        videos.append(vid)
                content.append({'content':i,'period':v,'videos':videos })
    g = str(individual.clas)
    if g == str('Nursery') or g == str('Prep I') or g == str('Prep II'):
        c = 'pre'
    elif g == str('First') or g == str('Second') or g == str('Third') or g == str('Fourth') or g == str('Fifth') or g == str('Sixth') or g == str('Seventh') or g == str('Eighth'):
        c = 'primary'
    elif g == str('Ninth'):
        c = 'ninth'
    elif g == str('Tenth'):
        c = 'tenth'
    class_subjects = []
    if content == [] and prev_content == []:
        for i in ClassSubjects.objects.all():
            if str(individual.clas.code) == str(i.class_name.code):
                class_subjects.append(i)
                content = 'No'
                prev_content = 'No'
    slide = ''
    for i in range(11,16):
        if str(datetime.date.today().day) == str(i):
            slide = 'Kindly Submit Your Fees Before 15 , Otherwise Your Account Will Be Inactive'
    context = {
        'request': request ,
        'slide' : slide ,
        'class_subjects':class_subjects,  
        'user':user,
        'content':content,
        'prev_content':prev_content,
        'clas':c,
        'individual':individual,
        'exam':exam,
    }
    if pk:
        return render(request,'Indivisuals/Period.html',context)
    else:
        day = datetime.datetime.now().strftime("%A")
        if str(datetime.date.today()) <= str(individual.start_date - timedelta(days=1)):
            return render(request,'Indivisuals/BeforeStart.html',context)
        elif str(individual.active) == str('False'):
            return render(request,'Indivisuals/FeeNotSubmited.html',context)
        else:
            return render(request,'Indivisuals/Profile.html',context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Individuals'])
def ManageIndivisualRevisionSubjectView(View , individual , clas , subject):
    user = View.user.groups.values('name')
    individual = get_object_or_404(Indivisuals , code = individual)
    clas = get_object_or_404(Classes , code = clas)
    subject = get_object_or_404(Subjects , code = subject)
    content = get_list_or_404(Content , class_name = clas , subject = subject )
    context = {
        'user':user,
        'content':content,
        'individual':individual,
    }
    return render(View,'Indivisuals/Revision.html',context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Individuals'])
def ManageIndivisualDocumentsView(DocumentView , pk):
    user = DocumentView.user.groups.values('name')
    content = get_object_or_404(Content , pk = int(pk))
    images = []
    for img in Images.objects.all():
        if str(img.content.pk) == str(content.pk):
            images.append(img)
    context = {
        'user':user,
        'content':content,
        'images':images,
    }
    return render(DocumentView,'Indivisuals/Documents.html',context)
