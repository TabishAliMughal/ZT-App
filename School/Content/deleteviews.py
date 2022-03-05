from django.shortcuts import render , redirect , get_object_or_404 , get_list_or_404
from School.Requirments.models import *
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from Authentication.user_handeling import unauthenticated_user, allowed_users, admin_only

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Admin'])
def ManageClassDeleteView(request,pk):
    data = Classes.objects.filter(pk = pk).delete()
    return redirect('school:class')

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Admin'])
def ManageSubjectDeleteView(request,pk):
    data = Subjects.objects.filter(pk = pk).delete()
    return redirect('school:subject')

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Admin'])
def ManageClassSubjectsDeleteView(request,pk):
    data = ClassSubjects.objects.filter(pk = pk).delete()
    return redirect('school:class_subject')

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Admin'])
def ManageModuleDeleteView(request,pk):
    data = Module.objects.filter(pk = pk).delete()
    return redirect('school:module')

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Admin'])
def ManageContentDeleteView(request,pk):
    data = Content.objects.filter(pk = pk).delete()
    return redirect('school:content')

def ManageContentPictureDeleteView(request,pk):
    data = get_object_or_404(Images , pk = pk)
    content = data.content.pk
    data.delete()
    return redirect('school:content_edit',content)

def ManageExamCloseView(request,pk):
    data = get_object_or_404(ExamStatus , pk = pk)
    print(data.status)
    if str(data.status) != 'False':
        form = ExamForm({
            'exam_number' : data.exam_number ,
            'class_name' : data.class_name ,
            'subject' : data.subject ,
            'session' : data.session ,
            'status' : 'False',
            }or None, instance=data)
        form.save()
    else:
        form = ExamForm({
            'exam_number' : data.exam_number ,
            'class_name' : data.class_name ,
            'subject' : data.subject ,
            'session' : data.session ,
            'status' : 'True',
            }or None, instance=data)
        form.save()
    return redirect('school:exam')