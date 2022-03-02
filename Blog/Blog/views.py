from Creator.models import Creator
from Blog.Blog.forms import ManageBlogCreateForm 
from django.shortcuts import get_object_or_404, render,get_list_or_404
from .models import Blog, Type
from Blog.Post.models import Post, PostComment, PostReact, ReactTypes
from django.contrib.auth.decorators import login_required
from Authentication.user_handeling import allowed_users
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from django.contrib.auth.models import User



def ManageBlogListView(request):
    user = request.user.groups.values('name')
    blogs = []
    for k in Type.objects.all():
        blog_list = []
        for i in Blog.objects.all():
            if str(i.type.pk) == str(k.pk):
                reacts = int('0')
                types = []
                posts = int('0')
                comment = int('0')
                for v in Post.objects.all():
                    if int(i.pk) == int(v.blog.pk):
                        posts = posts + 1
                        post_reacts = []
                        for l in ReactTypes.objects.all():
                            for b in PostReact.objects.all():
                                if b.post.pk == v.pk and b.react.pk == l.pk:
                                    reacts = reacts + int('1')
                                    types.append(b.react)
                        for l in PostComment.objects.all():
                            if int(v.pk) == int(l.post.pk):
                                comment = comment + 1
                flow = []
                for d in ReactTypes.objects.all():
                    if int(types.count(d)) != int('0'):
                        flow.append({"type":d.icon,"count":int(types.count(d))})
                flow.sort(key=lambda x: x.get("count"))
                icons = flow[::-1]
                abc = ''
                blog_list.append({'blog' : i , 'posts' : posts , 'react' : reacts , 'comment' : comment,'icons':icons[:2]})
        blogs.append({"type" : k , "blogs" : blog_list})
    context = {
        'user' : user ,
        'blogs' : blogs ,
    }
    return render(request,'Blog/List.html',context)

def ManageUserBlogListView(request,pk=None):
    user = request.user.groups.values('name')
    blogs = []
    if pk:
        blog_user = int(get_object_or_404(Creator,pk = pk).pk)
    else:
        blog_user = int(get_object_or_404(Creator,user = request.user.pk).pk)
    for i in Blog.objects.all():
        if int(i.user) == blog_user:
            reacts = []
            posts = int('0')
            comment = int('0')
            for v in Post.objects.all():
                if int(i.pk) == int(v.blog.pk):
                    posts = posts + 1
                    post_reacts = []
                    for l in ReactTypes.objects.all():
                        try:
                            b = len(get_list_or_404(PostReact,post=v,react=l))
                            post_reacts.append({l.name : b})
                        except:
                            pass
                    if post_reacts not in reacts:
                        reacts.append(post_reacts)
            for l in PostComment.objects.all():
                if int(v.pk) == int(l.post.pk):
                    comment = comment + 1
            total_reacts = int('0')
            flow = []
            for p in ReactTypes.objects.all():
                for l in reacts:
                    for t in l:
                        if str(t.get(p.name)) != "None":
                            total_reacts = total_reacts+int(t.get(p.name))
                            flow.append({"type":p.icon,"count":int(t.get(p.name))})
            flow.sort(key=lambda x: x.get("count"))
            icons = flow[::-1]
            blogs.append({'blog' : i , 'posts' : posts , 'react' : total_reacts , 'comment' : comment,'icons':icons})
    context = {
        'user' : user ,
        'blogs' : blogs ,
    }
    return render(request,'Blog/User/List.html',context)

@login_required(login_url='not_authorized')
@allowed_users(allowed_roles=['Creator'])
def ManageBlogCreateView(request):
    user = request.user.groups.values('name')
    if request.method == 'POST':
        user = ''
        for i in Creator.objects.all():
            if int(get_object_or_404(User,pk= i.user.pk).pk) == int(request.user.pk):
                cur_user = i
        image = Image.open(request.FILES.get('image'))
        size = image.size
        image = image.convert('RGB')
        rsize = []
        rsize.append(int(275*1))
        rsize.append(int(275*(size[0]/size[1])))
        rimg = image.resize(((rsize[1]),(rsize[0])),Image.ANTIALIAS)
        img_io = BytesIO()
        rimg.save(img_io, format='JPEG', quality=100)
        img_content = ContentFile(img_io.getvalue(),"img.jpg" )
        form = ManageBlogCreateForm({
            'name' : request.POST.get('name') ,
            'description' : request.POST.get('description') ,
            'type' : request.POST.get('type') ,
            'user' : cur_user.pk ,
        },{
            'image' : img_content
        })
        form.save()
        context = {
            'user' : user ,
        }
        return render(request,'Blog/User/Created.html',context)
    else:
        form = ManageBlogCreateForm()
        context = {
            'user' : user ,
            'form' : form ,
        }
        return render(request,'Blog/User/Create.html',context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Creator'])
def ManageBlogEditView(request,pk):
    user = request.user.groups.values('name')
    blog = get_object_or_404(Blog , pk = pk)
    if request.method == 'POST':
        if request.FILES.get('image'):
            image = Image.open(request.FILES.get('image'))
            size = image.size
            image = image.convert('RGB')
            rsize = []
            rsize.append(int(275*1))
            rsize.append(int(275*(size[0]/size[1])))
            rimg = image.resize(((rsize[1]),(rsize[0])),Image.ANTIALIAS)
            img_io = BytesIO()
            rimg.save(img_io, format='JPEG', quality=100)
            img_content = ContentFile(img_io.getvalue(),"img.jpg" )
        else:
            img_content = request.FILES.get('image')
        form = ManageBlogCreateForm({
            'name' : request.POST.get('name') ,
            'description' : request.POST.get('description') ,
            'type' : request.POST.get('type') ,
            'user' : blog.user ,
        } or None,{
            'image' : img_content ,
        } or None,instance=blog)
        form.save()
        context = {
            'user' : user ,
        }
        return render(request,'Blog/User/Created.html',context)
    else:
        form = ManageBlogCreateForm(instance = blog)
        context = {
            'user' : user ,
            'form' : form ,
        }
        return render(request,'Blog/User/Edit.html',context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Creator'])
def ManageBlogDeleteView(request,pk):
    user = request.user.groups.values('name')
    blog = get_object_or_404(Blog,pk = pk)
    blog.delete()
    context = {
        'user' : user ,
    }
    return render(request,'Blog/User/Deleted.html',context)
