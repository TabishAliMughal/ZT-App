from django.shortcuts import get_object_or_404, render , redirect
from django.contrib.auth.models import Group
from App.Authentication.views import HandleUser
from App.User.models import Creator
from App.User.forms import ManageUserDataForm
from App.User.models import UserData
from School.Indivisuals.models import Indivisuals
from Shop.Orders.models import Order
from Shop.Shop.models import Shops
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm , PasswordChangeForm
from datetime import datetime
from django.core.mail import send_mail
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
from App.Authentication.user_handeling import allowed_users

@login_required(login_url='main_login')
def ManageUserProfileView(request):
    cur_user = []
    if request.user.is_authenticated:
        c_user = get_object_or_404(User , pk = request.user.pk)
        u_data = UserData.objects.all().filter(user = c_user)
        address = []
        for i in u_data:
            if i.address:
                lat = (i.address[1])
                lng = (i.address[0])
                address = {'lat':lat , 'lng':lng}
        cur_user.append({'user' : c_user , 'data' : u_data , 'address' : address })
    context = {
        'cur_user' : cur_user ,
    }
    return render(request,'Profile/Profile.html',context)

def ManageUserProfileEditView(request):
    if request.method == 'POST':
        if request.FILES.get('picture'):
            image = Image.open(request.FILES.get('picture'))
            size = image.size
            image = image.convert('RGB')
            rsize = []
            rsize.append(int(275*1))
            rsize.append(int(275*(size[0]/size[1])))
            rimg = image.resize(((rsize[1]),(rsize[0])),Image.ANTIALIAS)
            img_io = BytesIO()
            rimg.save(img_io, format='JPEG', quality=75)
            img_content = ContentFile(img_io.getvalue(),"img.jpg" )
            try:
                user_data_form = ManageUserDataForm(request.POST or None , {'picture':img_content} , instance = get_object_or_404(UserData , user = request.user))
                user_data_form.save()
            except:
                user_data_form = ManageUserDataForm(request.POST or None , {'picture':img_content})
                user_data_form.save()
        try:
            user_change_form = UserChangeForm(request.POST or None , instance = get_object_or_404(User ,pk = request.user.pk) or None)
        except:
            user_change_form = UserChangeForm(request.POST or None)
        user_change_form.save()
        return redirect('user:user_profle')
    else:
        lat = ''
        lon = ''
        user_change_form = UserChangeForm(instance = get_object_or_404(User , pk = request.user.pk))
        try:
            user_data_form = ManageUserDataForm(instance = get_object_or_404(UserData , user = request.user))
            data =  get_object_or_404(UserData , user = request.user)
            lat = data.address[1]
            lon = data.address[0]
        except:
            user_data_form = ManageUserDataForm()
        context = {
            'lat' : lat ,
            'lon' : lon ,
            'user_data_form' : user_data_form ,
            'user_change_form' : user_change_form ,
        }
        return render(request,'Profile/Edit.html',context)

def ManageUserAccessView(request):
    context = {
    }
    return render(request,'Profile/ManageAccess.html',context)

def ManageUserChangeAccessToShopView(request):
    groups = request.user.groups.values('name')
    from django.contrib.auth.hashers import check_password
    if check_password(request.POST.get('password'),request.user.password) == True :
        for i in Order.objects.all().filter(user = get_object_or_404(UserData , user = request.user).pk):
            if str(i.status) != "Delivered":
                context = {
                    'message' : "Orders Pending",
                }
                return render(request,'Profile/ManageAccess.html',context)
        for i in groups:
            if str(i.get('name')) == "Shop_Public":
                request.user.groups.remove(Group.objects.get(name='Shop_Public'))
                request.user.groups.add(Group.objects.get(name='Shop_Creator'))
                HandleUser(request)
        return redirect('user:user_profle')
    else:
        context = {
            'message' : "Password Incorrect",
            'form' : "id_form_shop"
        }
        return render(request,'Profile/ManageAccess.html',context)
    

def ManageUserChangeAccessToBlogView(request):
    groups = request.user.groups.values('name')
    from django.contrib.auth.hashers import check_password
    if check_password(request.POST.get('password'),request.user.password) == True :
        for i in groups:
            if str(i.get('name')) == "Blog_Public":
                request.user.groups.remove(Group.objects.get(name='Blog_Public'))
                request.user.groups.add(Group.objects.get(name='Blog_Creator'))
                HandleUser(request)
        return redirect('user:user_profle')
    else:
        context = {
            'message' : "Password Incorrect",
            'form' : "id_form_blog"
        }
        return render(request,'Profile/ManageAccess.html',context)
