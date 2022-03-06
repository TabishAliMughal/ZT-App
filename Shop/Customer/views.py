from django.shortcuts import get_object_or_404, render , redirect
from App.User.models import UserData
from Shop.Orders.models import OrderItem , Order
from Shop.Orders.forms import OrderCreateForm
from Shop.Cart.cart import Cart
from App.Authentication.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group , User
from App.Authentication.user_handeling import unauthenticated_user, allowed_users, admin_only
import random
from .forms import *


@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Public'])
def ManagePreviousOrderView(request):
    user = request.user.groups.values('name')
    orders = []
    for i in Order.objects.all():
        if int(i.user) == int(get_object_or_404(UserData , user = request.user).pk):
            items = []
            for v in OrderItem.objects.all():
                if str(i.pk) == str(v.order.pk):
                    items.append(v)
            orders.append({'pk': i.pk , 'order' : i , 'items' : items })
    context = {
        'user' : user,
        'orders': orders,
    }
    return render(request,'orders/history/list.html',context)

