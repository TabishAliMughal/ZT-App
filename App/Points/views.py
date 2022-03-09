import re
from django.shortcuts import get_object_or_404, render
from App.User.models import UserData
from Blog.Blog.models import Blog
from Blog.Post.models import Post , PostComment , PostReact, ReactTypes



def ManageUserPointsView(request):
    cur_user = get_object_or_404(UserData , user = request.user )
    # For Shop
    # For Blog
    t_blogs = int('0')
    t_posts = int('0')
    t_blog_views = int('0')
    t_post_views = int('0')
    for i in Blog.objects.all().filter(user = cur_user.pk):
        t_blogs = t_blogs + int('1')
        t_blog_views = t_blog_views + i.views
        for j in Post.objects.all().filter(blog = i):
            t_posts = t_posts + int('1')
            t_post_views = t_post_views + j.views
    total_blog_points = int(t_blog_views)
    total_post_points = int(t_post_views/10)
    total_reacts = []
    for i in ReactTypes.objects.all():
        total_reacts_count = int('0')
        for p in PostReact.objects.all().filter(react = i):
            if int(p.post.blog.user) == int(cur_user.pk) :
                total_reacts_count = total_reacts_count + 1
        total_reacts.append({'type':i,'total':total_reacts_count , 'points' : (total_reacts_count*i.points_add)-(total_reacts_count*i.points_subtract)})
    total_react_points = sum([i.get('points') for i in total_reacts])
    blog_status = {
        'total_reacts':total_reacts,
        'total_react_points':total_react_points,
        'total_posts' : t_posts,
        'total_post_views' : t_post_views,
        'total_post_points' : total_post_points,
        'total_blogs' : t_blogs,
        'total_blog_views' : total_blog_points,
        'total_blog_points' : total_blog_points,
        'total_points' : int(total_react_points + total_post_points + total_blog_points)
    }
    context = {
        'blog_status' : blog_status ,
    }
    return render(request,'Points/List.html',context)


    # t_blogs = int('0')
    # t_posts = int('0')
    # blog_status = []
    # for i in Blog.objects.all().filter(user = cur_user.pk):
    #     t_blogs = t_blogs + int('1')
    #     reacts = []
    #     for j in Post.objects.all().filter(blog = i):
    #         t_posts = t_posts + int('1')
    #         # for k in PostReact.objects.all().filter(post = j):
    #         #     react_points_add = react_points_add + int(k.react.points_add)
    #         #     react_points_subtract = react_points_subtract + int(k.react.points_add)
    #         for m in ReactTypes.objects.all():
    #             react_points_add = int('0')
    #             react_points_subtract = int('0')
    #             for n in PostReact.objects.all().filter(react = m,post = j):
    #                 react_points_add = react_points_add + int(n.react.points_add)
    #                 react_points_subtract = react_points_subtract + int(n.react.points_add)
    #             if react_points_add != int('0') and react_points_subtract != int('0'):
    #                 reacts.append({'post' : j , 'type' : m , 'react_points_add' : react_points_add ,'react_points_subtract' : react_points_subtract })
    #     if reacts != []:
    #         blog_status.append({'blog': i , 'reacts' : reacts })
    # blog_result = {'total_blogs':t_blogs , 'total_posts':t_posts , 'status':blog_status}
    # print(blog_result)