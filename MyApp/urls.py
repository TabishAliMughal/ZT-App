"""MyShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from Main import views
from MyApp.admin import blogsite , shopsite , matrinomialsite , schoolsite

urlpatterns = [
    # Login Redirect
    path('accounts/profile/',views.ManageAuth),
    path('social-auth/complete/facebook',views.ManageAuth),
    path('social-auth/rejected/facebook',views.Rejected),
    path('social-auth/',include('social_django.urls', namespace='shop_social')),
    # Main Urls
    path('', include('Main.urls')),
    path('blogsite/', blogsite.urls),
    path('shopsite/', shopsite.urls),
    path('adminsite/', admin.site.urls),
    path('schoolsite/', schoolsite.urls),
    path('matrinomialsite/', matrinomialsite.urls),
    path('creator/', include('Creator.urls', namespace='creator')),
    path('user/log/', include('Authentication.urls', namespace='auth')),
    # Shop Urls
    path('shopping/', include('Shop.Shop.urls', namespace='shop')),
    path('shopping/cart/', include('Shop.Cart.urls', namespace='shop_cart')),
    path('shopping/orders/', include('Shop.Orders.urls', namespace='shop_orders')),
    path('shopping/accounts/', include('Shop.Accounts.urls', namespace='shop_account')),
    path('shopping/costumer/', include('Shop.Customer.urls', namespace='shop_costumer')),
    path('shopping/delivery/', include('Shop.Delivery.urls', namespace='shop_delivery')),
    # Blog Urls
    path('blog/',include('Blog.Blog.urls', namespace='blog_blog')),
    path('blog/tags/',include('Blog.Tags.urls', namespace='blog_tags')),
    path('blog/post/',include('Blog.Post.urls', namespace='blog_post')),
    path('blog/bunch/',include('Blog.Bunch.urls', namespace='blog_bunch')),
    # School Urls
    path('school/', include('School.Content.urls', namespace='school')),
    path('school/exam/', include('School.Exam.urls', namespace='school_exam')),
    path('school/admin/', include('School.Admin.urls',namespace='school_admin')),
    path('school/result/', include('School.Result.urls', namespace='school_result')),
    path('school/teacher/', include('School.Teacher.urls', namespace='school_teacher')),
    path('school/checker/', include('School.Checker.urls', namespace='school_checker')),
    path('school/visitor/', include('School.Visitors.urls', namespace='school_visitors')),
    path('school/school/', include('School.RegSchool.urls', namespace='school_reg_school')),
    path('school/indivisuals/', include('School.Indivisuals.urls', namespace='school_individuals')),
    # Relationships Urls
    path('candidate/', include('Relationships.Candidate.urls', namespace='candidate')),
    path('relationships/', include('Relationships.Info.urls', namespace='relationships')),
    path('relationships/match/', include('Relationships.Matching.urls', namespace='relationships_matching')),
]
handler404 = "Main.views.PageNotFoundView"
handler500 = "Main.views.PageNotFoundView"