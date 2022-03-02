from django.shortcuts import render , get_list_or_404 , get_object_or_404 , redirect , HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group , User
from Authentication.user_handeling import unauthenticated_user, allowed_users, admin_only
from .models import *
from .forms import *
from School.Content.models import *
from School.Exam.models import *
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile


@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Teacher'])
def ManageTeacherProfileView(request):
    equal = ''
    exam = []
    classes = []
    user = request.user.groups.values('name')
    teacher = request.user
    # Classes
    for i in TeacherClass.objects.all():
        if str(i.teacher) == str(teacher):
            classes.append(i)
    # Exams
    for i in ExamStatus.objects.all():
        for v in classes:
            if str(i.class_name.pk) == str(v.clas.pk):
                if str(i.status) == 'True':
                    exam.append(i)
                else:
                    exam = ['No Active Exams']
            else:
                exam = ['No Active Exams']
    # -------------------
    if classes == []:
        classes = 'No Class'
    context = {
        'exam': exam ,
        'user': user ,
        'class' : classes ,
        'teacher': teacher ,
        'equal' : equal ,
    }
    return render(request,'Teacher/Profile.html',context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Teacher'])
def ManageTeacherClassView(request,id):
    user = request.user.groups.values('name')
    exam = ''
    classtud = []
    classes = []
    tea = request.user
    teacherclass = get_object_or_404(TeacherClass , pk = id)
    for i in TeacherClass.objects.all():
        if str(i.teacher) == str(tea):
            classes.append(i)
    for i in TeacherClassStudents.objects.all():
        if str(i.clas.pk) == str(id):
            classtud.append(i)
    for i in ExamStatus.objects.all():
        for v in classes:
            if str(i.class_name.pk) == str(v.clas.pk):
                if str(i.status) == 'True':
                    exam = 'Active'
                else:
                    exam = 'No Active Exams'
            else:
                exam = 'No Active Exams'
    context = {
        'exam': exam ,
        'teacherclass': teacherclass ,
        'user': user ,
        'class' : classtud ,
    }
    return render(request,'Teacher/Display/Class.html',context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Teacher'])
def TeacherClassCreateView(request,id):
    user = request.user.groups.values('name')
    teacher = request.user
    if request.method == 'POST':
        rawdata = request.POST
        clas = rawdata.get("clas")
        school = rawdata.get("school")
        geolocation = rawdata.get("location")
        form = TeacherClassCreateForm({
            'teacher' : teacher ,
            'session' : int('1') ,
            'clas' : clas ,
            'limit' : 5 ,
            'school' : school ,
            'location' : geolocation ,
        })
        if form.is_valid:
            form.save()
        return redirect('school_teacher:teacher_profile')
    else:
        form = TeacherClassCreateForm()
        context = {
            'user': user ,
            'form': form ,
            'teacher': teacher ,
        }
        return render(request,'Teacher/Create/Class.html',context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Teacher'])
def ManageAddStudentView(request,id):
    user = request.user.groups.values('name')
    if request.method == 'POST':
        clas = id
        name = request.POST.get('name')
        father = request.POST.get('father_name')
        contact = request.POST.get('contact')
        address = request.POST.get('address')
        if request.FILES.get('picture'):
            image = Image.open(request.FILES.getlist('picture'))
            size = image.size
            image = image.convert('RGB')
            rsize = []
            rsize.append(int(275*1))
            rsize.append(int(275*(size[0]/size[1])))
            rimg = image.resize(((rsize[1]),(rsize[0])),Image.ANTIALIAS)
            img_io = BytesIO()
            rimg.save(img_io, format='JPEG', quality=100)
            img_content = ContentFile(img_io.getvalue(),"img.jpg" )
        else:
            img_content = request.FILES.get('picture')
        if str(picture) == '':
            picture = 'null'
        form = TeacherClassStudentCreateForm({
            'clas' : clas ,
            'name' : name ,
            'father_name' : father ,
            'contact' : contact ,
            'address' : address ,
            'picture' : img_content ,
        })
        form.save()
        return redirect('school_teacher:teacher_class',id)
    else:
        clas = get_object_or_404(TeacherClass,pk = id)
        limit = ''
        count = '0'
        form = TeacherClassStudentCreateForm()
        for i in TeacherClassStudents.objects.all():
            if str(i.clas.teacher.pk) == str(request.user.pk):
                count = int(count) + 1
                if str(count) >= str(clas.limit):
                    limit = 'Reached'
        context = {
            'limit': limit ,
            'class': clas ,
            'form': form ,
            'user': user ,
        }
        return render(request,'Teacher/Create/Student.html',context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Teacher'])
def ManageEditStudentView(request,id,pk):
    student = get_object_or_404(TeacherClassStudents, pk = pk)
    if request.method == 'POST':
        clas = id
        name = request.POST.get('name')
        father = request.POST.get('father_name')
        contact = request.POST.get('contact')
        address = request.POST.get('address')
        if request.FILES.get('picture'):
            image = Image.open(request.FILES.get('picture'))
            size = image.size
            image = image.convert('RGB')
            rsize = []
            rsize.append(int(275*1))
            rsize.append(int(275*(size[0]/size[1])))
            rimg = image.resize(((rsize[1]),(rsize[0])),Image.ANTIALIAS)
            img_io = BytesIO()
            rimg.save(img_io, format='JPEG', quality=100)
            img_content = ContentFile(img_io.getvalue(),"img.jpg" )
        else:
            img_content = request.FILES.get('picture')
        form = TeacherClassStudentCreateForm({
            'clas' : clas ,
            'name' : name ,
            'father_name' : father ,
            'contact' : contact ,
            'address' : address ,
        } or None,{
            'picture' : img_content ,
        } or None , instance=student)
        form.save()
        return redirect('school_teacher:teacher_class',id)
    else:
        clas = get_object_or_404(TeacherClass,pk = id)
        user = request.user.groups.values('name')
        form = TeacherClassStudentCreateForm(instance=student)
        context = {
            'class': clas ,
            'form': form ,
            'user': user ,
        }
        return render(request,'Teacher/Edit/Student.html',context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Teacher'])
def ManageDeleteStudentView(request,id,pk):
    TeacherClassStudents.objects.filter(pk = pk).delete()
    return redirect('school_teacher:teacher_class',id)

