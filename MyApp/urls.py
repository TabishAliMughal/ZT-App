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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from MyApp import settings
from MyApp.admin import blogsite , shopsite , matrinomialsite

urlpatterns = [
    # Login Redirect
    path('accounts/profile/',views.ManageAuth),
    path('social-auth/complete/facebook',views.ManageAuth),
    path('social-auth/rejected/facebook',views.Rejected),
    path('social-auth/',include('social_django.urls', namespace='shop_social')),
    # Main Urls
    path('', include('Main.urls')),
    path('adminsite/', admin.site.urls),
    path('blogsite/', blogsite.urls),
    path('shopsite/', shopsite.urls),
    path('matrinomialsite/', matrinomialsite.urls),
    path('creator/', include('Creator.urls', namespace='creator')),
    path('user/log/', include('Authentication.urls', namespace='auth')),
    # Shop Urls
    path('shopping/', include('Shop.Shop.urls', namespace='shop')),
    path('shopping/accounts/', include('Shop.Accounts.urls', namespace='shop_account')),
    path('shopping/cart/', include('Shop.Cart.urls', namespace='shop_cart')),
    path('shopping/orders/', include('Shop.Orders.urls', namespace='shop_orders')),
    path('shopping/costumer/', include('Shop.Customer.urls', namespace='shop_costumer')),
    path('shopping/delivery/', include('Shop.Delivery.urls', namespace='shop_delivery')),
    # Blog Urls
    path('blog/',include('Blog.Blog.urls', namespace='blog')),
    path('blog/bunch/',include('Blog.Bunch.urls', namespace='bunch')),
    path('blog/post/',include('Blog.Post.urls', namespace='post')),
    # School Urls
    path('school/', include('School.School.urls', namespace='school')),
    # Relationships Urls
    path('relationships/', include('Relationships.Info.urls', namespace='relationships')),
    path('candidate/', include('Relationships.Candidate.urls', namespace='candidate')),
    path('relationships/match/', include('Relationships.Matching.urls', namespace='relationships_matching')),
]
# if settings.DEBUG:
#     urlpatterns += staticfiles_urlpatterns()

handler404 = "Main.views.PageNotFoundView"
handler500 = "Main.views.PageNotFoundView"