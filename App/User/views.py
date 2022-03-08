# from django.shortcuts import get_object_or_404, redirect, render
# import random
# from django.contrib.auth.models import Group , User
# from App.Authentication.forms import UserCreationForm
# # from .forms import ManageCreatorCreateForm
# from .models import Creator
# from django.contrib.auth import authenticate, login


# def ManageCreatorCreateView(request):
#     if request.method == 'POST':
#         data = request.POST
#         user = ''
#         for i in data.get("name"):
#             if str(i) != ' ':
#                 user = str(user) + str(i.lower())
#         user_form = UserCreationForm({
#             'username' : data.get('name') ,
#             'email' : '{}@123'.format(user.lower()) ,
#             'password1' : data.get('password') ,
#             'password2' : data.get('password') ,
#         })
#         try:
#             k = user_form.save()
#         except:
#             context = {
#                 'user' : user ,
#                 'message' : { 'first' : 'Error' , 'second' : 'Another Account With Same Username Exist'}
#             }
#             return render(request , 'creator/created.html' , context)
#         groups = Group.objects.get(name='Creator')
#         k.groups.add(groups)
#         form = ManageCreatorCreateForm({
#             'name' : data.get('name') ,
#             'user' : k ,
#             'mobile' : data.get('mobile') ,
#             'nic' : data.get('nic') ,
#             'bank_account' : data.get('bank_account') ,
#             'easypaisa' : data.get('easypaisa') ,
#         })
#         form.save()
#         user = authenticate(request, username=data.get("name"), password=data.get("password"))
#         if user is not None:
#             login(request, user)
#         user = request.user.groups.values('name')
#         context = {
#             'user' : user ,
#             'message' : { 'first' : 'Thank You!' , 'second' : 'Your account Has Been Created'}
#         }
#         return render(request , 'creator/created.html' , context)
#     return redirect('main')

from django.shortcuts import get_object_or_404, render , redirect
# from App.User.forms import ManageCreatorCreateForm
from django.contrib.auth.models import Group
from App.User.models import Creator
from App.User.forms import ManageUserDataForm
from App.User.models import UserData
from School.Indivisuals.models import Indivisuals
from Shop.Shop.models import Shops
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm , PasswordChangeForm
from datetime import datetime
from django.core.mail import send_mail
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile


def ManageUserProfileView(request):
    user = request.user.groups.values('name')
    cur_user = []
    if request.user.is_authenticated:
        c_user = get_object_or_404(User , pk = request.user.pk)
        u_data = UserData.objects.all().filter(user = c_user)
        address = []
        for i in u_data:
            lat = (i.address[1])
            lng = (i.address[0])
            address = {'lat':lat , 'lng':lng}
        cur_user.append({'user' : c_user , 'data' : u_data , 'address' : address })
    context = {
        'user' : user ,
        'cur_user' : cur_user ,
    }
    return render(request,'Profile/Profile.html',context)

def ManageUserProfileEditView(request):
    user = request.user.groups.values('name')
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
            # print(get_object_or_404(UserData , user = request.user))
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
        print(user_change_form)
        context = {
            'user' : user ,
            'lat' : lat ,
            'lon' : lon ,
            'user_data_form' : user_data_form ,
            'user_change_form' : user_change_form ,
        }
        return render(request,'Profile/Edit.html',context)
