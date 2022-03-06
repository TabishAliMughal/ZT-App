from django.shortcuts import get_object_or_404, render , redirect
from App.User.forms import ManageCreatorCreateForm
from django.contrib.auth.models import Group
from App.User.models import Creator, UserData
from School.Indivisuals.models import Indivisuals
from Shop.Shop.models import Shops
from django.contrib.auth.models import User
from App.User.forms import ManageUserDataForm

def ManageAuth(request):
    group = Group.objects.get(name='Public')
    request.user.groups.add(group)
    user = get_object_or_404(User , pk = request.user)
    try:
        user_data_form = ManageUserDataForm({'first_name':user.first_name}or None , instance = get_object_or_404(UserData , user = request.user)).save()
    except:
        user_data_form = ManageUserDataForm({'first_name':user.first_name}).save()
    return redirect('main')

def Rejected(request):
    user = request.user.groups.values('name')
    context = {
        'user' : user ,
    }
    return render(request,'Includes/Rejected.html',context)

def PrivicyPolicy(request):
    user = request.user.groups.values('name')
    context = {
        'user' : user ,
    }
    return render(request,'PrivacyPolicy.html',context)

def TermsAndConditions(request):
    user = request.user.groups.values('name')
    context = {
        'user' : user ,
    }
    return render(request,'TermsAndConditions.html',context)

def NotAuthorized(request):
    user = request.user.groups.values('name')
    context = {
        'user' : user ,
    }
    return render(request,'Includes/NotAuthorized.html',context)

def ManageMainPage(request):
    user = request.user.groups.values('name')
    form = ManageCreatorCreateForm()
    shop = 'NoShop'
    student = 'no student'
    if request.user.is_authenticated:
        for i in user:
            if i.get('name') == 'Creator':
                try:
                    shop = get_object_or_404(Shops , user = (get_object_or_404(Creator , user = request.user.pk)).pk)
                except:
                    pass
            if i.get('name') == 'Public':
                try:
                    student = get_object_or_404(Indivisuals , user = request.user.pk)
                except:
                    pass
    context = {
        'user' : user ,
        'form' : form ,
        'shop' : shop ,
        'student' : student ,
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

def ManageAboutUsView(request):
    user = request.user.groups.values('name')
    context = {
        'user' : user ,
    }
    return render(request,'AboutUs.html',context)