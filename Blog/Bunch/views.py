from webbrowser import get
from django.shortcuts import redirect, render , HttpResponseRedirect , get_object_or_404
from Blog.Blog.models import Blog
from Blog.Post.models import Post
from App.Creator.models import Creator
from .models import Bunch, BunchPost
from .forms import ManageBunchCreateForm , ManageBunchPostCreateForm
from django.contrib.auth.decorators import login_required
from App.Authentication.user_handeling import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.models import User




def ManageBunchListView(request,blog=None):
    user = request.user.groups.values('name')
    bunch = []
    l = int('0')
    if blog :
        blog = Blog.objects.all().order_by('time').filter(pk = blog)
    else:
        blog = Blog.objects.all().order_by('time')
    for i in Bunch.objects.all():
        for v in blog:
            if int(i.blog.pk) == int(v.pk):
                posts = []
                for k in BunchPost.objects.all().order_by('serial'):
                    if int(k.bunch.pk) == int(i.pk):
                        posts.append(k.post)
                bunch.append({'number' : l ,'bunch' : i , 'post' : posts})
                l = l + 1
    context = {
        'user' : user ,
        'bunch' : bunch ,
    }
    return render(request,'bunch/list.html',context)

def ManageBunchNextPostView(request,bunch):
    user = request.user.groups.values('name')
    bunch = get_object_or_404(Bunch , pk = bunch)
    context = {
        'user' : user ,
        'bunch' : bunch ,
    }
    return render(request,'bunch/list.html',context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Creator'])
def ManageBunchCreateView(request):
    user = request.user.groups.values('name')
    if request.method == 'POST':
        if not request.POST.get('blog'):
            bunch = get_object_or_404(Bunch,name = request.POST.get('name'))
            blog = get_object_or_404(Blog,pk = bunch.blog.pk)
            posts = Post.objects.all().order_by('time').filter(blog = blog)
            posts1 = []
            for i in posts:
                posts1.append(i)
            sel_posts = []
            for i in posts :
                for k in BunchPost.objects.all().order_by('serial'):
                    if str(bunch.pk) == str(k.bunch.pk):
                        if k.post.pk == i.pk:
                            sel_posts.append(i)
                            posts1.remove(i)
            context = {
                'user' : user ,
                'bunch' : bunch ,
                'posts' : posts ,
                'posts' : posts1 ,
                'sel_posts' : sel_posts ,
            }
            return render(request,'bunch/add_post.html',context)
        form = ManageBunchCreateForm({
            'name' : request.POST.get('name') ,
            'blog' : request.POST.get('blog') ,
        })
        bunch = form.save()
        bunch = get_object_or_404(Bunch,name = request.POST.get('name'))
        blog = get_object_or_404(Blog,pk = bunch.blog.pk)
        posts = Post.objects.all().order_by('time').filter(blog = blog)
        context = {
            'user' : user ,
            'bunch' : bunch ,
            'posts' : posts ,
        }
        return render(request,'bunch/add_post.html',context)
    else:
        form = ManageBunchCreateForm()
        blog = []
        for i in Blog.objects.all().order_by('time'):
            if int(i.user) == int(get_object_or_404(Creator,user = request.user.pk).pk):
                blog.append(i)
        context = {
            'user' : user ,
            'form' : form ,
            'blog' : blog ,
        }
        return render(request,'bunch/create.html',context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Creator'])
def BunchAddPostsView(request):
    if request.method == 'POST':
        bunch = get_object_or_404(Bunch,pk = (request.POST.get('bunch')))
        for i in BunchPost.objects.all().order_by('serial'):
            if int(i.bunch.pk) == int(request.POST.get('bunch')):
                i.delete()
        p = int('0')
        for v in request.POST.getlist('posts'):
            for i in Post.objects.all().order_by('time'):
                if int(i.pk) == int(v):
                    form = ManageBunchPostCreateForm({
                        'bunch' : request.POST.get('bunch') ,
                        'post' : i ,
                        'serial' : p ,
                    })
                    if form.is_valid:
                        form.save()
                        p = int(p)+int('1')
    return redirect('blog_bunch:blog_bunch_list',bunch.blog.pk)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Creator'])
def ManageBunchEditView(request,bunch):
    user = request.user.groups.values('name')
    bunch = get_object_or_404(Bunch , pk = bunch)
    if request.method == 'POST':
        form = ManageBunchCreateForm({
            'name' : request.POST.get('name') ,
            'blog' : bunch.blog ,
        } or None,instance=bunch)
        form.save()
        context = {
            'user' : user ,
        }
        return render(request,'bunch/created.html',context)
    else:
        form = ManageBunchCreateForm(instance = bunch)
        blog = bunch.blog
        context = {
            'user' : user ,
            'blog' : blog ,
            'form' : form ,
        }
        return render(request,'bunch/edit.html',context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Creator'])
def ManageBunchDeleteView(request,bunch):
    user = request.user.groups.values('name')
    bunch = get_object_or_404(Bunch,pk = bunch)
    bunch.delete()
    context = {
        'user' : user ,
    }
    return render(request,'bunch/deleted.html',context)

