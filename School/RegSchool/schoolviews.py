from django.shortcuts import render , get_object_or_404 , get_list_or_404 , redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group , User
from App.Authentication.user_handeling import unauthenticated_user, allowed_users, admin_only
from School.Teacher.models import *
from School.Checker.models import *
from .forms import *
from School.Indivisuals.models import *


@login_required(login_url='main_login')
@allowed_users(allowed_roles=['School'])
def ManageSchoolProfileView(request):
    groups = Group.objects.all()
    group = ''
    for i in groups:
        if str(i) == 'Teacher':
            group = i
    user = request.user.groups.values('name')
    log_school = request.user
    s = School.objects.all()
    school = []
    teachers = []
    students = []
    v = TeacherClass.objects.all()
    for i in v:
        if str(i.school) != 'None':
            if str(i.school.user.pk) == str(log_school.pk):
                teachers.append(i)
    for i in s:
        if str(i.user.pk) == str(log_school.pk):
            school.append(i)
    if school == []:
        school = 'No'
    for i in Indivisuals.objects.all():
        if str(i.school) != 'None':
            if str(i.school.user.pk) == str(log_school.pk):
                students.append(i)
    context = {
        'user' : user ,
        'school': school ,
        'teachers': teachers ,
        'students': students ,
        'user': user ,
    }
    return render(request,'School/Profile.html',context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Admin','School'])
def ManageTeacherProfileDetailView(request , id):
    user = request.user.groups.values('name')
    asked = get_object_or_404(User,pk = id)
    students = '0'
    clas = []
    classes = []
    teachers = Group.objects.get(name="Teacher")
    teachers = teachers.user_set.all()
    for t in teachers:
        if str(t.pk) == str(asked.pk):
            for i in TeacherClass.objects.all():
                if str(i.teacher.pk) == str(id):
                    classes.append(i.clas)
            for i in TeacherClassStudents.objects.all():
                if str(i.clas.teacher.pk) == str(id):
                    clas.append(i.name)
            for i in clas:
                students = int(students) + 1
            context = {
                'classes' : classes ,
                'students' : students ,
                'user': user ,
                'teacher' : asked
            }
            return render(request,'Teacher/ProfileDetail.html',context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['School'])
def ManageSchoolCreateView(request):
    user = request.user.groups.values('name')
    if request.method == "POST":
        rawdata = request.POST
        school = rawdata.get('school')
        address = rawdata.get('address')
        form = ManageSchoolCreateForm({
            'school': school ,
            'address': address ,
            'user': request.user.pk
        })
        form.save()
        return redirect('school_reg_school:school_profile')
    else:
        form = ManageSchoolCreateForm()
        context = {
            'form' : form ,
            'user': user ,
        }
        return render(request,'School/Create/School.html',context)