from django.shortcuts import render , redirect , get_object_or_404 , get_list_or_404
from School.Requirments.models import *
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from Authentication.user_handeling import unauthenticated_user, allowed_users, admin_only
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile


@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Admin'])
def ManageClassesCreateView(request):
    if request.method == 'POST':
        form = ClassesForm(request.POST)
        user = request.user.groups.values('name')
        if form.is_valid:
            form.save()
            context = { 
                'user':user ,
                'return': 'Has Been Added SuccessFully'
            }
            return render(request,'Forms/Created/classes.html',context)
        else:
            context = { 
                'user':user ,
                'return': 'Is Not Valid'
            }
            return render(request,'Forms/Created/classes.html',context)
    else:
        form = ClassesForm()
        user = request.user.groups.values('name')
        context = { 
            'user':user ,
            'form': form
        }
        return render(request , 'Forms/Create/classes.html' , context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Admin'])
def ManageSubjectsCreateView(request):
    user = request.user.groups.values('name')
    if request.method == 'POST':
        form = SubjectsForm(request.POST)
        if form.is_valid:
            form.save()
            context = { 
                'user':user ,
                'user':user ,
                'return': 'Has Been Added SuccessFully'
            }
            return render(request,'Forms/Created/subjects.html',context)
        else:
            context = { 
                'user':user ,
                'return': 'Is Not Valid'
            }
            return render(request,'Forms/Created/subjects.html',context)
    else:
        form = SubjectsForm()
        context = { 
            'user':user ,
            'form': form
        }
        return render(request ,'Forms/Create/subjects.html', context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Admin'])
def ManageClassSubjectsCreateView(request):
    user = request.user.groups.values('name')
    if request.method == 'POST':
        clas = request.POST.get('class_name')
        subj = request.POST.getlist('sub' , default='1')
        for i in subj:
            form = ClassSubjectsForm({
                'class_name' : clas ,
                'subject_name' : i ,
            })
            if form.is_valid:
                form.save()
        context = { 
            'user':user ,
            'return': 'Has Been Added SuccessFully'
        }
        return render(request,'Forms/Created/classsubjects.html',context)
    else:
        form = ClassSubjectsForm()
        subject = Subjects.objects.all()
        context = { 
            'user':user ,
            'form': form ,
            'sub' : subject ,
        }
        return render(request ,'Forms/Create/classsubjects.html', context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Admin'])
def ManageModuleCreateView(request):
    user = request.user.groups.values('name')
    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid:
            form.save()
            context = { 
                'user':user ,
                'return': 'Has Been Added SuccessFully'
            }
            return render(request,'Forms/Created/module.html',context)
        else:
            context = { 
                'user':user ,
                'return': 'Is Not Valid'
            }
            return render(request,'Forms/Created/module.html',context)
    else:
        form = ModuleForm()
        context = { 
            'user':user ,
            'form': form
        }
        return render(request ,'Forms/Create/module.html', context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Admin','DataHandler'])
def ManageContentCreateView(request):
    user = request.user.groups.values('name')
    if request.method == 'POST':
        data = request.POST
        form1 = ContentForm(request.POST)
        k = ''
        if form1.is_valid:
            k = form1.save()
            url = data.getlist('url')
            v = int('0')
            for i in url:
                form2 = VideoForm({
                    'content' : k ,
                    'url' : url[v]
                })
                v = v + 1
                form2.save()
            l = int('0')
            for v in request.FILES.getlist('image'):
                image = Image.open(request.FILES.getlist('image')[l])
                size = image.size
                image = image.convert('RGB')
                rsize = []
                rsize.append(int(275*1))
                rsize.append(int(275*(size[0]/size[1])))
                rimg = image.resize(((rsize[1]),(rsize[0])),Image.ANTIALIAS)
                img_io = BytesIO()
                rimg.save(img_io, format='JPEG', quality=100)
                img_content = ContentFile(img_io.getvalue(),"img.jpg" )
                form3 = ImageForm({
                    'content' : k ,
                },{
                    'image' : img_content ,
                })
                l = l + 1
                form3.save()
            context = { 
                'user':user ,
                'return': 'Has Been Added SuccessFully'
            }
            return render(request,'Forms/Created/content.html',context)
        else:
            context = { 
                'user':user ,
                'return': 'Is Not Valid'
            }
            return render(request,'Forms/Created/content.html',context)
    else:
        form1 = ContentForm()
        form2 = VideoForm()
        form3 = ImageForm()
        context = { 
            'user':user ,
            'form1': form1,
            'form2': form2,
            'form3': form3,
        }
        return render(request ,'Forms/Create/content.html', context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Admin'])
def ManageExamCreateView(request):
    user = request.user.groups.values('name')
    if request.method == 'POST':
        form = ExamForm({
            'exam_number' : request.POST.get('exam_number') ,
            'class_name' : request.POST.get('class_name') ,
            'subject' : request.POST.get('subject') ,
            'session' : request.POST.get('session') ,
            'status' : 'True' ,
        })
        if form.is_valid:
            form.save()
            context = { 
                'user':user ,
                'return': 'Has Been Added SuccessFully'
            }
            return render(request,'Forms/Created/exam.html',context)
        else:
            context = { 
                'user':user ,
                'return': 'Is Not Valid'
            }
            return render(request,'Forms/Created/exam.html',context)
    else:
        form = ExamForm()
        context = { 
            'user':user ,
            'form': form
        }
        return render(request ,'Forms/Create/exam.html', context)