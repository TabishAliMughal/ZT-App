from Blog.Blog.models import Blog
from Blog.Post.models import Post
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from App.Authentication.user_handeling import allowed_users
from .models import Tags , BlogTags , PostTags
from .forms import ManageTagsCreateForm , ManagePostTagsCreateForm , ManageBlogTagsCreateForm
from App.User.models import Creator, UserData


@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Blog_Creator'])
def ManageBlogAddTagsView(request,pk):
    blog = get_object_or_404(Blog , pk = pk)
    if request.method == 'POST':
        for i in BlogTags.objects.all().filter(blog = blog):
            i.delete()
        for i in request.POST.getlist('tags'):
            try:
                tag = get_object_or_404(Tags , name = str(i.replace(' ','_').replace('#','')))
            except:
                tag = ManageTagsCreateForm({'name' : i.replace(' ','_').replace('#','')})
                print(tag)
                tag.save()
            BlogTags.objects.update_or_create(blog = blog , tag = tag)
        return redirect('blog_post:post_list_by_blog',blog.pk)
    else:
        selected_tags = BlogTags.objects.all().filter(blog = blog.pk)
        tags = Tags.objects.all()
        context = {
            'selected_tags' : selected_tags ,
            'tags' : tags ,
        }
        return render(request,'Tags/Blog/Tags.html',context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Blog_Creator'])
def ManagePostAddTagsView(request,pk):
    post = get_object_or_404(Post , pk = pk)
    if request.method == 'POST':
        for i in PostTags.objects.all().filter(post = post):
            i.delete()
        for i in request.POST.getlist('tags'):
            try:
                tag = get_object_or_404(Tags , name = str(i.replace(' ','_').replace('#','')))
            except:
                tag = ManageTagsCreateForm({'name' : i.replace(' ','_').replace('#','')}).save()
            PostTags.objects.update_or_create(post = post , tag = tag)
        return redirect('blog_post:post_list_by_blog',post.blog.pk)
    else:
        selected_tags = PostTags.objects.all().filter(post = post.pk)
        tags = Tags.objects.all()
        context = {
            'selected_tags' : selected_tags ,
            'tags' : tags ,
        }
        return render(request,'Tags/Post/Tags.html',context)

def ManageTagsListView(request):
    tags = Tags.objects.all()
    context = {
        'tags' : tags ,
    }
    return render(request,'Tags/List.html',context)

def ManageTagDetailView(request,pk):
    tag = get_object_or_404(Tags , pk = pk)
    blogs = BlogTags.objects.all().filter(tag = tag)
    for i in blogs:
        blog_user = get_object_or_404(UserData , pk = i.blog.user)
        i.blog_user = blog_user
    posts = PostTags.objects.all().filter(tag = tag)
    context = {
        'tag' : tag ,
        'blogs' : blogs ,
        'posts' : posts ,
    }
    return render(request,'Tags/Detail.html',context)
