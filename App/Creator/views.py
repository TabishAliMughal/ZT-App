from django.shortcuts import get_object_or_404, redirect, render
import random
from django.contrib.auth.models import Group , User
from App.Authentication.forms import UserCreationForm
from .forms import ManageCreatorCreateForm
from .models import Creator
from django.contrib.auth import authenticate, login


def ManageCreatorCreateView(request):
    if request.method == 'POST':
        data = request.POST
        user = ''
        for i in data.get("name"):
            if str(i) != ' ':
                user = str(user) + str(i.lower())
        user_form = UserCreationForm({
            'username' : data.get('name') ,
            'email' : '{}@123'.format(user.lower()) ,
            'password1' : data.get('password') ,
            'password2' : data.get('password') ,
        })
        try:
            k = user_form.save()
        except:
            context = {
                'user' : user ,
                'message' : { 'first' : 'Error' , 'second' : 'Another Account With Same Username Exist'}
            }
            return render(request , 'creator/created.html' , context)
        groups = Group.objects.get(name='Creator')
        k.groups.add(groups)
        form = ManageCreatorCreateForm({
            'name' : data.get('name') ,
            'user' : k ,
            'mobile' : data.get('mobile') ,
            'nic' : data.get('nic') ,
            'bank_account' : data.get('bank_account') ,
            'easypaisa' : data.get('easypaisa') ,
        })
        form.save()
        user = authenticate(request, username=data.get("name"), password=data.get("password"))
        if user is not None:
            login(request, user)
        user = request.user.groups.values('name')
        context = {
            'user' : user ,
            'message' : { 'first' : 'Thank You!' , 'second' : 'Your account Has Been Created'}
        }
        return render(request , 'creator/created.html' , context)
    return redirect('main')

def ManageCreatorProfileView(request):
    user = request.user.groups.values('name')
    creator = get_object_or_404(Creator,user = request.user)
    
    context = {
        'user' : user ,
        'creator' : creator ,
    }
    return render(request , 'creator/profile.html' , context)

