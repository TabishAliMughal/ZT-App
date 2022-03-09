from django.shortcuts import get_object_or_404, render , redirect
from App.User.models import UserData
from Shop.Orders.models import OrderItem , Order, OrderReview
from Shop.Orders.forms import OrderCreateForm
from Shop.Cart.cart import Cart
from App.Authentication.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group , User
from App.Authentication.user_handeling import unauthenticated_user, allowed_users, admin_only
import random
from .forms import *


@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Shop_Public'])
def ManagePreviousOrderView(request):
    orders = []
    for i in Order.objects.all():
        if int(i.user) == int(get_object_or_404(UserData , user = request.user).pk):
            items = []
            for v in OrderItem.objects.all():
                if str(i.pk) == str(v.order.pk):
                    items.append(v)
            try:
                review = range(0,get_object_or_404(OrderReview , order = i).stars)
            except:
                review = None
            orders.append({'pk': i.pk , 'order' : i , 'items' : items , 'review' : review})
    orders = orders[::-1]
    context = {
        'orders': orders,
    }
    return render(request,'Orders/History/List.html',context)

