import re
from django.shortcuts import render , redirect
from Creator.forms import ManageCreatorCreateForm
from django.contrib.auth.models import Group

def ManageAuth(request):
    group = Group.objects.get(name='Public')
    request.user.groups.add(group)
    return redirect('main')

def Rejected(request):
    user = request.user.groups.values('name')
    context = {
        'user' : user ,
    }
    return render(request,'Includes/Rejected.html',context)

def NotAuthorized(request):
    user = request.user.groups.values('name')
    context = {
        'user' : user ,
    }
    return render(request,'Includes/NotAuthorized.html',context)

def ManageMainPage(request):
    user = request.user.groups.values('name')
    form = ManageCreatorCreateForm()
    context = {
        'user' : user ,
        'form' : form ,
    }
    return render(request,'Main.html',context)

def ManageMainPageLogin(request):
    user = request.user.groups.values('name')
    form = ManageCreatorCreateForm()
    context = {
        'user' : user ,
        'form' : form ,
        'login' : 'True' ,
    }
    return render(request,'Main.html',context)

def PageNotFoundView(request,exception=None):
    user = request.user.groups.values('name')
    context = {
        'user' : user ,
    }
    return render(request,'Includes/404.html',context)
