from django.shortcuts import render , get_object_or_404 , get_list_or_404 , redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group , User
from App.Authentication.user_handeling import unauthenticated_user, allowed_users, admin_only
from School.Teacher.models import *
from School.Checker.models import *
from School.Indivisuals.models import *
from School.Indivisuals.forms import *
import datetime
from .current import get_all_logged_in_users


@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Admin'])
def ManageProfilesView(request):
    checkers = Group.objects.get(name="Checker")
    checkers = checkers.user_set.all()
    teachers = Group.objects.get(name="Teacher")
    teachers = teachers.user_set.all()
    individualuser = Group.objects.get(name="Individuals")
    individualuser = individualuser.user_set.all()
    individuals = []
    i_act = int('0')
    i_deact = int('0')
    for i in Indivisuals.objects.all():
        if i.school == None :
            if i.active == True:
                i_act = i_act + 1
            else:
                i_deact = i_deact + 1
    stud = {'active':i_act,'deactive':i_deact,'total':(i_act)+(i_deact)}
    individuals.append({'students':stud})
    schools = []
    for s in School.objects.all():
        act = int('0')
        deact = int('0')
        for i in Indivisuals.objects.all():
            if i.school != None:
                if str(s.pk) == str(i.school.pk):
                    if i.active == True:
                        act = act + 1
                    else:
                        deact = deact + 1
        stud = {'active':act,'deactive':deact,'total':(act)+(deact)}
        schools.append({'school':s,'students':stud})
    students = []
    for i in TeacherClass.objects.all():
        stud = int('0')
        for stu in TeacherClassStudents.objects.all():
            if str(i.pk) == str(stu.clas.pk):
                stud = stud + 1
        students.append({'teacher':i.teacher,'students':stud})
    log_count = User.objects.filter(last_login__startswith=datetime.datetime.now().date()).count()
    users = (get_all_logged_in_users())
    p = int('0')
    for i in users:
        p = p + 1
    visit = Visits.objects.all()
    context = {
        'visit': visit ,
        'num_users': p ,
        'log_count': log_count ,
        'students': students ,
        'individuals': individuals ,
        'schoolstudents': schools,
        'checkers': checkers ,
        'teachers': teachers ,
    }
    return render(request,'Admin/Profiles.html',context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Admin'])
def ManageActiveAndDeactiveView(request):
    school = School.objects.all()
    individuals = Indivisuals.objects.all()
    if request.method == 'POST':
        data = request.POST
        if data.getlist('pk'):
            for i in data.getlist('pk'):
                individual = get_object_or_404(Indivisuals , pk = i)
                if str(data.get(i)) == 'on':
                    active = True
                else:
                    active = False
                form = IndivisualsForm({
                    'user' : individual.user ,
                    'session' : individual.session ,
                    'name' : individual.name ,
                    'father_name' : individual.father_name ,
                    'mobile' : individual.mobile ,
                    'school' : individual.school ,
                    'clas' : individual.clas ,
                    'fees' : individual.fees ,
                    'password' : individual.password ,
                    'active' : active ,
                } or None , instance = individual)
                form.save()
            return redirect('school_admin:active_deactive')
        if data.get('school'):
            if str(data.get('school')) != 'None':
                if str(data.get('school')) == 'Digital-School':
                    individuals = []
                    for i in Indivisuals.objects.all():
                        if str(i.school) == 'None':
                            individuals.append(i)
                else:
                    individuals = []
                    for i in Indivisuals.objects.all():
                        if str(i.school) != 'None':
                            if str(i.school.pk) == str(data.get('school')):
                                individuals.append(i)

            context = {
                'school': school ,
                'individuals': individuals ,
            }
            return render(request,'Admin/Activation/ByList.html',context)
    else:
        school = School.objects.all()
        individuals = Indivisuals.objects.all()
        context = {
            'school': school ,
            'individuals': individuals ,
        }
        return render(request,'Admin/Activation/ByList.html',context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Admin'])
def ManageActiveAndDeactiveBySchoolView(request):
    context = {
    }
    return render(request,'Admin/Activation/BySchool.html',context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Admin'])
def ManageActivateSchoolView(request):
    if request.method == 'POST':
        data = request.POST
        school = data.get('school')
        school = get_object_or_404(School , pk = school)
        for i in Indivisuals.objects.all():
            if str(i.school) != 'None':
                if str(i.school.pk) == str(school.pk):
                    individual = i
                    form = IndivisualsForm({
                        'user' : individual.user ,
                        'session' : individual.session ,
                        'name' : individual.name ,
                        'father_name' : individual.father_name ,
                        'mobile' : individual.mobile ,
                        'school' : individual.school ,
                        'clas' : individual.clas ,
                        'fees' : individual.fees ,
                        'password' : individual.password ,
                        'active' : True ,
                    } or None , instance = individual)
                    form.save()
        return redirect('school:main')
    else:
        school = School.objects.all()
        context = {
            'school': school ,
        }
        return render(request,'Admin/Activation/ActivateSchool.html',context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Admin'])
def ManageDeactivateSchoolView(request):
    if request.method == 'POST':
        data = request.POST
        school = data.get('school')
        school = get_object_or_404(School , pk = school)
        for i in Indivisuals.objects.all():
            if str(i.school) != 'None':
                if str(i.school.pk) == str(school.pk):
                    individual = i
                    form = IndivisualsForm({
                        'user' : individual.user ,
                        'session' : individual.session ,
                        'name' : individual.name ,
                        'father_name' : individual.father_name ,
                        'mobile' : individual.mobile ,
                        'school' : individual.school ,
                        'clas' : individual.clas ,
                        'fees' : individual.fees ,
                        'password' : individual.password ,
                        'active' : False ,
                    } or None , instance = individual)
                    form.save()
        return redirect('school:main')
    else:
        school = School.objects.all()
        context = {
            'school': school ,
        }
        return render(request,'Admin/Activation/DeactivateSchool.html',context)
    
