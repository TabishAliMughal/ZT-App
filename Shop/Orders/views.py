from django.shortcuts import render
from .models import OrderItem , Order
from .forms import OrderCreateForm , OrderItemsCreateForm
from Shop.Customer.models import UserData
from Shop.Cart.cart import Cart
from Shop.Shop.models import Product , Shops
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group , User
from Authentication.user_handeling import unauthenticated_user, allowed_users, admin_only
from Shop.Cart.calculations import LatLonCalculator
from Shop.Cart.models import DeliveryCharge
import random
import requests
import json



@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Public'])
def ManageOrderCreateView(request,user):
    user = request.user.groups.values('name')
    unorder_cart = Cart(request)
    cart = []
    curr_user = ''
    total_delivery = int('0')
    for i in Shops.objects.all():
        delivery = int('0')
        pro = []
        for v in unorder_cart:
            q = (v.get('quantity'))
            k = (v.get('total_price'))
            p = (v.get('product'))
            if int(i.pk) == int(p.shop.pk):
                pro.append({ 'product' : p , 'total_price' : k ,'quantity' : q})
        if pro != []:
            for u in UserData.objects.all():
                if int(u.user) == int(request.user.pk):
                    t = LatLonCalculator(u.address,i.address)
                    curr_user = u
                    for j in DeliveryCharge.objects.all():
                        delivery = int(j.compulsory) + (int(j.per_km)*int(t))
                        total_delivery = total_delivery + delivery
                        break
            cart.append({'shop': i , 'item' : pro , 'delivery' : delivery})
    if request.method == 'POST':
        order = []
        if cart:
            for i in cart:
                order_form = OrderCreateForm({
                    'user' : curr_user ,
                    'paid' : False ,
                    'status' : "Pending" ,
                    'price' : sum(t.get('total_price')for t in i.get('item')) ,
                    'delivery' : i.get('delivery') ,
                })
                if order_form.is_valid():
                    sav_ord_form = order_form.save()
                    order.append(sav_ord_form)
                    for l in (i.get('item')):
                        item_form = OrderItemsCreateForm({
                            'order' : sav_ord_form ,
                            'product' : l.get('product') ,
                            'price' : l.get('total_price') ,
                            'quantity' : l.get('quantity') ,
                        })
                        item_form.save()
            unorder_cart.clear()
            context = {
                'user' : user,
                'order': order
                }
            return render(request,'orders/order/created.html',context)
        else:
            return render(request,'error.html',{'return' : 'Plese Select Some Items'})
    else:
        user = []
        for i in UserData.objects.all():
            if str(i.user) == str(request.user.pk):
                user.append(i)
        address = []
        for i in user:
            address = ({'lat':i.address[1],'lon':i.address[0]})
        form = OrderCreateForm()
        context = {
            'delivery': total_delivery,
            'u_cart' : unorder_cart ,
            'address': address ,
            'user':user,
            'user' : user,
            'cart': cart,
            'form': form
            }
        return render(request,'orders/order/create.html',context)

