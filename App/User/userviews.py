from django.shortcuts import get_object_or_404, render , redirect
from App.User.forms import ManageCreatorCreateForm
from django.contrib.auth.models import Group
from App.User.models import Creator
from App.Main.forms import ManageUserPictureForm
from App.Main.models import UserPicture
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
        image = UserPicture.objects.all().filter(user = c_user)
        cur_user.append({'user' : c_user , 'image' : image })
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
            try:
                picture_form = ManageUserPictureForm(request.POST or None , {'picture':img_content} , instance = get_object_or_404(UserPicture , user = request.user))
            except:
                picture_form = ManageUserPictureForm(request.POST or None , {'picture':img_content})
            picture_form.save()
        try:
            user_change_form = UserChangeForm(request.POST or None , instance = get_object_or_404(User ,pk = request.user.pk) or None)
        except:
            user_change_form = UserChangeForm(request.POST or None)
        user_change_form.save()
        return redirect('user_profle')
    else:
        user_change_form = UserChangeForm(instance = get_object_or_404(User , pk = request.user.pk))
        try:
            picture_form = ManageUserPictureForm(instance = get_object_or_404(UserPicture , user = request.user))
        except:
            picture_form = ManageUserPictureForm()
        context = {
            'user' : user ,
            'picture_form' : picture_form ,
            'user_change_form' : user_change_form ,
        }
        return render(request,'Profile/Edit.html',context)
