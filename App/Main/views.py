from django.shortcuts import get_object_or_404, render , redirect
# from App.User.forms import ManageCreatorCreateForm
from django.contrib.auth.models import Group
from App.User.models import Creator, UserData
from School.Indivisuals.models import Indivisuals
from Shop.Shop.models import Shops
from django.contrib.auth.models import User
from App.User.forms import ManageUserDataForm

def ManageAuth(request):
    request.user.groups.add(Group.objects.get(name='Shop_Public'))
    request.user.groups.add(Group.objects.get(name='School_Public'))
    request.user.groups.add(Group.objects.get(name='Blog_Public'))
    request.user.groups.add(Group.objects.get(name='Matrinomial_Public'))
    user = request.user.groups.values('name')
    request.session['user'] = [i.get('name') for i in user]
    request.session.save()
    user = get_object_or_404(User , pk = request.user.pk)
    try:
        ManageUserDataForm({'user':user ,'first_name':user.first_name}or None , instance = get_object_or_404(UserData , user = request.user)).save()
    except:
        ManageUserDataForm({'user':user ,'first_name':user.first_name}).save()
    return redirect('main')

def Rejected(request):
    context = {
    }
    return render(request,'Includes/Rejected.html',context)

def PrivicyPolicy(request):
    context = {
    }
    return render(request,'PrivacyPolicy.html',context)

def TermsAndConditions(request):
    context = {
    }
    return render(request,'TermsAndConditions.html',context)

def NotAuthorized(request):
    context = {
    }
    return render(request,'Includes/NotAuthorized.html',context)

def ManageMainPage(request):
    user = request.user.groups.values('name')
    shop = 'NoShop'
    student = 'NoStudent'
    if request.user.is_authenticated:
        for i in user:
            if i.get('name') == 'Shop_Creator':
                try:
                    shop = get_object_or_404(Shops , user = (get_object_or_404(UserData , user = request.user.pk)).pk)
                except:
                    pass
            if i.get('name') == 'School_Public':
                try:
                    student = get_object_or_404(Indivisuals , user = request.user.pk)
                except:
                    pass
    context = {
        'shop' : shop ,
        'student' : student ,
    }
    return render(request,'Main.html',context)

def ManageMainPageLogin(request):
    # form = ManageCreatorCreateForm()
    context = {
        # 'form' : form ,
        'login' : 'True' ,
    }
    return render(request,'Main.html',context)

def PageNotFoundView(request,exception=None):
    context = {
    }
    return render(request,'Includes/404.html',context)

def ManageAboutUsView(request):
    context = {
    }
    return render(request,'AboutUs.html',context)