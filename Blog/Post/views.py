from django.http.response import HttpResponseRedirect
from Blog.Blog.models import Blog
from django.shortcuts import get_object_or_404, redirect, render
from .models import Post, PostComment, PostReact, ReactTypes
from .forms import ManagePostCommentForm, ManagePostCreateForm, ManagePostReactForm
from django.contrib.auth.decorators import login_required
from Authentication.user_handeling import unauthenticated_user, allowed_users, admin_only
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from django.contrib.auth.models import User


def ManagePostListView(request,pk=None):
    user = request.user.groups.values('name')
    posts = []
    post = []
    blog = ''
    if pk:
        blog = get_object_or_404(Blog , pk = pk)
        for i in Post.objects.all():
            if int(i.blog.pk) == int(blog.pk):
                post.append(i)
    else:
        for i in Post.objects.all():
            post.append(i)
    for l in post:
        reacts = []
        for k in ReactTypes.objects.all():
            v = int('0')
            for i in PostReact.objects.all():
                if int(i.react.pk) == int(k.pk):
                    if int(i.post.pk) == int(l.pk):
                        v = v + 1
            reacts.append({'type' : k , 'total' : v })
        try:
            length = int(100/len(reacts))
        except:
            length = int('0')
        posts.append({'post' : l , 'reacts' : reacts , 'width' : length })
    context = {
        'user' : user ,
        'blog' : blog ,
        'posts' : posts,
    }
    return render(request,'post/list.html',context)

def ManagePostDetailView(request,pk):
    user = request.user.groups.values('name')
    post = get_object_or_404(Post , pk = pk)
    react = []
    for k in ReactTypes.objects.all():
        v = int('0')
        for i in PostReact.objects.all():
            if int(i.post.pk) == int(post.pk):
                if int(i.react.pk) == int(k.pk):
                    v = v + 1
        react.append({'type' : k , 'total' : v})
    comments = []
    v = int('0')
    comment = []
    for i in PostComment.objects.all():
        if int(post.pk) == int(i.post.pk):
            comment.append({
                'user' : get_object_or_404(User,pk = i.user) ,
                'post' : i.post ,
                'comment' : i.comment ,
            })
            v = v + 1
    comments = {'comment' : comment , 'total' : v}
    if int(len(post.text)) >= int('150'):
        setattr(post,'stext',post.text[:150])
        setattr(post,'ltext',post.text[150:])
    context = {
        'react' : react ,
        'user' : user ,
        'post' : post ,
        'comments' : comments ,
    }
    return render(request,'post/detail.html',context)

@login_required(login_url='main_login')
def ManagePostReactView(request,pk):
    post = get_object_or_404(Post , pk = pk)
    try:
        get_object_or_404(PostReact , user = request.user.pk , post = post).delete()
    except:
        pass
    form = ManagePostReactForm({
        'user' : request.user.pk ,
        'post' : post ,
        'react' : int(request.POST.get('react'))
    })
    form.save()
    return redirect('post:post_detail',post.pk)

@login_required(login_url='main_login')
def ManagePostCommentView(request,pk):
    post = get_object_or_404(Post , pk = pk)
    form = ManagePostCommentForm({
        'user' : request.user.pk ,
        'post' : post ,
        'comment' : request.POST.get('comment')
    })
    form.save()
    return redirect('post:post_detail',post.pk)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Creator'])
def ManagePostCreateView(request,pk):
    user = request.user.groups.values('name')
    if request.method == 'POST':
        user = ''
        blog = get_object_or_404(Blog , pk = pk)
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
        form = ManagePostCreateForm({
            'name' : request.POST.get('name') ,
            'description' : request.POST.get('description') ,
            'text' : request.POST.get('text') ,
            'video' : request.POST.get('video') ,
            'blog' : blog ,
        },{
            'sound' : request.FILES.get('sound') ,
            'image' : img_content ,
        })
        form.save()
        context = {
            'blog' : blog ,
            'user' : user ,
        }
        return render(request,'post/created.html',context)
    else:
        form = ManagePostCreateForm()
        context = {
            'user' : user ,
            'form' : form ,
        }
        return render(request,'post/create.html',context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Creator'])
def ManagePostEditView(request,pk):
    user = request.user.groups.values('name')
    post = get_object_or_404(Post , pk = pk)
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
        form = ManagePostCreateForm({
            'name' : request.POST.get('name') ,
            'description' : request.POST.get('description') ,
            'text' : request.POST.get('text') ,
            'video' : request.POST.get('video') ,
            'blog' : post.blog ,
        } or None,{
            'sound' : request.FILES.get('sound') ,
            'image' : img_content ,
        } or None,instance=post)
        form.save()
        context = {
            'blog' : post.blog ,
            'user' : user ,
        }
        return render(request,'post/created.html',context)
    else:
        form = ManagePostCreateForm(instance = post)
        context = {
            'user' : user ,
            'form' : form ,
        }
        return render(request,'post/edit.html',context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Creator'])
def ManagePostDeleteView(request,pk):
    user = request.user.groups.values('name')
    post = get_object_or_404(Post,pk = pk)
    blog = post.blog
    post.delete()
    context = {
        'user' : user ,
        'blog' : blog ,
    }
    return render(request,'post/deleted.html',context)

