from datetime import datetime
from django.shortcuts import render , redirect , get_object_or_404
from .models import *
from .forms import *
from App.Authentication.forms import *
import random
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group , User
from App.Authentication.user_handeling import unauthenticated_user, allowed_users, admin_only


@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Admin','School'])
def ManageIndivisualsListView(request):
    indivisual = Indivisuals.objects.all()
    if request.method == 'POST':
        if str(request.POST.get('school')) != str('None'):
            indivisual = []
            for i in Indivisuals.objects.all():
                if i.school :
                    if str(request.POST.get('school')) == str(i.school.pk):
                        indivisual.append(i)
        if str(request.POST.get('school')) == str('Digital-School'):
            indivisual = []
            for i in Indivisuals.objects.all():
                if i.school :
                    pass
                else:
                    indivisual.append(i)
    v = int('0')
    for i in indivisual:
        v = v + 1
    school = School.objects.all()
    context = {
        'school' : school ,
        'indivisual' : indivisual ,
        'total' : v ,
    }
    return render(request , 'Indivisuals/list.html' , context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Admin','School','School_Public'])
def ManageIndivisualsCreateView(request , pk=None):
    user = request.user.groups.values('name')
    if pk:
        school = get_object_or_404(School , pk = pk)
    else:
        school = 'No'
    if request.method == 'POST':
        data = request.POST
        for i in user:
            if str(i.get('name')) == 'Admin' or str(i.get('name')) == 'School':
                username = ""
                for i in data.get('name'):
                    if str(i) != ' ':
                        username = str(username) + str(i.lower())
                for i in data.get('father_name'):
                    if str(i) != ' ':
                        username = str(username) + str(i.lower())
                p = ['a','b','c','d','e','1','2','3','4','5']
                random.shuffle(p)
                pas = ''
                for i in range(0,4):
                    pas = pas + p[i]
                password = '{}@123'.format(pas)
                user_form = CreateUserForm({
                    'username' : username ,
                    'email' : '{}@gmail.com'.format(username) ,
                    'password1' : password ,
                    'password2' : password ,
                })
                user_form.save()
                seluser = User.objects.get(username = username)
                redirect_page = 'admin'
                group = Group.objects.get(name='Individuals')
                seluser.groups.add(group)
                break
            if str(i.get('name')) == 'School_Public':
                # seluser = User.objects.get(pk = request.user.pk)
                seluser = get_object_or_404(User,pk = request.user.pk)
                redirect_page = 'School_Public'
                password = 'no password'
        # print(seluser)
                group = Group.objects.get(name='School_Public')
                seluser.groups.remove(group)
                group = Group.objects.get(name='Individuals')
                seluser.groups.add(group)
                break
        form = IndivisualsForm({
            'start_date' : data.get('start_date') ,
            'user' : seluser.pk ,
            'name' : data.get('name') ,
            'father_name' : data.get('father_name') ,
            'school' : data.get('school') ,
            'mobile' : data.get('mobile') ,
            'clas' : data.get('clas') ,
            'fees' : data.get('fees') ,
            'password' : password ,
            'active' : data.get('active') ,
        })
        form.save()
        if redirect_page == 'admin':
            return redirect('school_individuals:indivisuals_list')
        if redirect_page == 'School_Public':
            return redirect('school_individuals:indivisual_profile')
    else:
        form = IndivisualsForm()
        date = datetime.today().strftime('%Y-%m-%d')
        context = {
            'school' : school ,
            'form' : form ,
            'date' : date ,
        }
        return render(request , 'Indivisuals/Create/create.html' , context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Admin','School'])
def ManageIndivisualsDetailView(request , pk):
    indivisual = get_object_or_404(Indivisuals , pk = pk)
    context = {
        'indivisual' : indivisual ,
    }
    return render(request , 'Indivisuals/detail.html' , context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Admin','School'])
def ManageIndivisualsEditView(request , pk):
    indivisual = get_object_or_404(Indivisuals , pk = pk)
    if request.method == 'POST':
        data = request.POST
        form = IndivisualsForm({
            'user' : indivisual.user ,
            'name' : data.get('name') ,
            'father_name' : data.get('father_name') ,
            'school' : data.get('school') ,
            'start_date': data.get('start_date') ,
            'mobile' : data.get('mobile') ,
            'clas' : data.get('clas') ,
            'fees' : data.get('fees') ,
            'password' : indivisual.password ,
            'active' : data.get('active') ,
        }or None , instance = indivisual)
        form.save()
        return redirect('school_individuals:indivisuals_detail',indivisual.pk)
    else:
        form = IndivisualsForm(instance = indivisual)
        date = datetime.today().strftime('%Y-%m-%d')
        context = {
            'form' : form ,
            'date' : date ,
        }
        return render(request , 'Indivisuals/edit.html' , context)
    
@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Admin','School'])
def ManageIndivisualsDeleteView(request , pk):
    indivisual = get_object_or_404(Indivisuals , pk = pk)
    user = indivisual.user
    user.delete()
    indivisual.delete()
    return redirect('school_individuals:indivisuals_list')

