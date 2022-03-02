from django.shortcuts import render , redirect
from Shop.Orders.models import OrderItem , Order
from Shop.Orders.forms import OrderCreateForm
from Shop.Cart.cart import Cart
from Authentication.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group , User
from Authentication.user_handeling import unauthenticated_user, allowed_users, admin_only
import random
from .forms import *


@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Public'])
def ManagePreviousOrderView(request):
    user = request.user.groups.values('name')
    orders = []
    for i in Order.objects.all():
        if str(i.user.user) == str(request.user.pk):
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


@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Public'])
def ManageCostumerDataView(request):
    user = request.user.groups.values('name')
    data = ''
    lat = ''
    lon = ''
    for i in UserData.objects.all():
        if str(i.user) == str(request.user.pk):
            data = i
    form = ManageCreateUserDataForm()
    if data != '':
        form = ManageCreateUserDataForm(instance = data)
        lat = data.address[1]
        lon = data.address[0]
    if request.method == 'POST':
        group = Group.objects.get(name='Public')
        request.user.groups.add(group)
        form = ManageCreateUserDataForm({
            'user' : request.user.pk ,
            'first_name' : request.POST.get('first_name'),
            'address' : request.POST.get('address'),
            'city' : request.POST.get('city'),
        })
        if data:
            form = ManageCreateUserDataForm({
                'user' : request.user.pk ,
                'first_name' : request.POST.get('first_name'),
                'address' : request.POST.get('address'),
                'city' : request.POST.get('city'),
            } or None , instance = data)
        if form.is_valid():
            form.save()
        return redirect('/')
    else:
        context = {
            'user' : user ,
            'form': form ,
            'lat' : lat ,
            'lon' : lon ,
        }
        return render(request,'costumer/CreateData.html',context)