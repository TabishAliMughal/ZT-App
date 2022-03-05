from django.shortcuts import render , redirect , get_object_or_404 , get_list_or_404
from School.Requirments.models import *
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from App.Authentication.user_handeling import unauthenticated_user, allowed_users, admin_only
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Admin'])
def ManageClassEditView(request,pk):
    user = request.user.groups.values('name')
    data = get_object_or_404(Classes, pk = pk)
    if request.method == 'POST':
        form = ClassesForm(request.POST or None, instance=data)
        if form.is_valid:
            form.save()
            return redirect('school:class')
    else:
        form = ClassesForm(instance=data)
        context = {
            'form' : form,
            'user':user ,
        }
        return render(request, 'Forms/Edit/classes.html' , context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Admin'])
def ManageSubjectEditView(request,pk):
    user = request.user.groups.values('name')
    data = get_object_or_404(Subjects, pk = pk)
    if request.method == 'POST':
        form = SubjectsForm(request.POST or None, instance=data)
        if form.is_valid:
            form.save()
            return redirect('school:subject')
    else:
        form = SubjectsForm(instance=data)
        context = {
            'user':user ,
            'form' : form,
        }
        return render(request,'Forms/Edit/subjects.html' , context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Admin'])
def ManageClassSubjectsEditView(request,pk):
    user = request.user.groups.values('name')
    data = get_object_or_404(ClassSubjects, pk = pk)
    if request.method == 'POST':
        form = ClassSubjectsForm(request.POST or None, instance=data)
        if form.is_valid:
            form.save()
            return redirect('school:class_subject')
    else:
        form = ClassSubjectsForm(instance=data)
        context = {
            'user':user ,
            'form' : form,
        }
        return render(request,'Forms/Edit/classsubjects.html' , context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Admin'])
def ManageModuleEditView(request,pk):
    user = request.user.groups.values('name')
    data = get_object_or_404(Module, pk = pk)
    if request.method == 'POST':
        form = ModuleForm(request.POST or None, instance=data)
        if form.is_valid:
            form.save()
            return redirect('school:module')
    else:
        form = ModuleForm(instance=data)
        context = {
            'user':user ,
            'form' : form,
        }
        return render(request,'Forms/Edit/module.html' , context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Admin','DataHandler'])
def ManageContentEditView(request,pk):
    user = request.user.groups.values('name')
    data = get_object_or_404(Content, pk = pk)
    videos = []
    for i in Videos.objects.all():
        if str(i.content.pk) == str(data.pk):
            videos.append(i)
    images = []
    l = int('0')
    for i in Images.objects.all():
        if str(i.content.pk) == str(data.pk):
            images.append(i)
            l = l + 1
    if request.method == 'POST':
        vid = request.POST
        form = ContentForm(request.POST or None, instance=data)
        if form.is_valid:
            form.save()
            url = vid.getlist('url')
            p = int('0')
            for i in url:
                p = p+1
            v = int('0')
            for i in videos:
                i.delete()
            for i in url:
                form2 = VideoForm({
                    'content' : data.pk ,
                    'url' : url[v]
                })
                v = v + 1
                form2.save()            
            p = int('0')
            for i in request.FILES.getlist('image'):
                image = Image.open(request.FILES.getlist('image')[i])
                size = image.size
                image = image.convert('RGB')
                rsize = []
                rsize.append(int(275*1))
                rsize.append(int(275*(size[0]/size[1])))
                rimg = image.resize(((rsize[1]),(rsize[0])),Image.ANTIALIAS)
                img_io = BytesIO()
                rimg.save(img_io, format='JPEG', quality=75)
                img_content = ContentFile(img_io.getvalue(),"img.jpg" )
                form2 = ImageForm({
                    'content' : data.pk ,
                },{
                    'image' : img_content
                })
                p = p + 1
                form2.save()
            return redirect('school:content')
    else:
        form = ContentForm(instance=data)
        context = {
            'user':user ,
            'form' : form ,
            'videos' : videos ,
            'images' : images ,
        }
        return render(request,'Forms/Edit/content.html' , context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Admin'])
def ManageExamEditView(request,pk):
    user = request.user.groups.values('name')
    data = get_object_or_404(ExamStatus, pk = pk)
    if request.method == 'POST':
        form = ExamForm(request.POST or None, instance=data)
        if form.is_valid:
            form.save()
            return redirect('school:exam')
    else:
        form = ExamForm(instance=data)
        context = {
            'user':user ,
            'form' : form,
        }
        return render(request,'Forms/Edit/exam.html' , context)