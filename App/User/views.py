from django.shortcuts import get_object_or_404, render , redirect
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
from django.contrib.auth.decorators import login_required
from App.Authentication.user_handeling import allowed_users

@login_required(login_url='main_login')
def ManageUserProfileView(request):
    cur_user = []
    if request.user.is_authenticated:
        c_user = get_object_or_404(User , user = request.user.pk)
        u_data = UserData.objects.all().filter(user = c_user)
        address = []
        for i in u_data:
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
    return render(request,'Profile/Profile.html',context)
