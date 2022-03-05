from django.shortcuts import render, get_object_or_404 , get_list_or_404
from Shop.Orders.models import Order , OrderItem
from Shop.Accounts.models import ShopkeperPayment , ShopAdminShare , DeliveryPersonPayment , DeliveryAdminShare
from Shop.Shop.models import Shops
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group , User
from Authentication.user_handeling import unauthenticated_user, allowed_users, admin_only
from .forms import ManageShopkeperPaymentForm , ManageDeliveryPersonPaymentForm , ManagePaymentProofForm
from Shop.Delivery.models import DeliveryTasks , DeliveryPerson
import math
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile


@login_required(login_url='auth:login_url')
@allowed_users(allowed_roles=['Creator'])
def ManageShopAccountView(request):
    user = request.user.groups.values('name')
    unpaid_orders = []
    paid_orders = []
    cur_shop = ''
    for k in Shops.objects.all():
        if int(k.user) == int(request.user.pk):
            cur_shop = k.pk
    for i in Order.objects.all():
        for p in OrderItem.objects.all():
            if int(p.order.pk) == int(i.pk):
                shop = p.product.shop.pk
        if str(cur_shop) == str(shop):
            for v in ShopkeperPayment.objects.all():
                if str(i.status) == 'Delivered':
                    if int(i.pk) == int(v.order.pk):
                        paid_orders.append(i)
                    else:
                        unpaid_orders.append(i)
    context = {
        'unpaid_orders' : unpaid_orders ,
        'paid_orders' : paid_orders ,
        'user' : user ,
    }
    return render(request,'accounts/shop.html',context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Admin'])
def ManageShopAccountPaymentListView(request):
    user = request.user.groups.values('name')
    payments = ShopkeperPayment.objects.all()
    orders = []
    for i in Order.objects.all():
        shop_paid = []
        for v in ShopkeperPayment.objects.all():
            if int(i.pk) == int(v.order.pk):
                shop_paid = 'True'
        delivery_paid = []
        for v in DeliveryPersonPayment.objects.all():
            if int(i.pk) == int(v.order.pk):
                delivery_paid = 'True'
        if str(i.status) == 'Delivered':
            orders.append({'order' : i , 'shop' : shop_paid , 'delivery' : delivery_paid})
    context = {
        'user' : user ,
        'payments' : payments ,
        'orders' : orders ,
    }
    return render(request,'accounts/payment/list.html',context)

def ManageShopAccountPaymentPayView(request):
    user = request.user.groups.values('name')
    form = ManageShopkeperPaymentForm()
    shop_product = []
    for i in ShopAdminShare.objects.all():
        admin_share = int(i.share_percentage)
    for k in Shops.objects.all():
        tot_price = int('0')
        final_orders = []
        orders = []
        for i in OrderItem.objects.all():
            if int(i.product.shop.pk) == int(k.pk):
                for p in Order.objects.all():
                    if str(p.status) == 'Delivered':
                        if int(i.order.pk) == int(p.pk):
                            if p not in orders:
                                orders.append(p)
        for g in ShopkeperPayment.objects.all():
            for p in orders:
                if int(g.order.pk) == int(p.pk):
                    orders.remove(p)
        if orders != []:
            for i in orders:
                final_orders.append({'orders':i  , 'price' : math.trunc(i.price-i.price/100*admin_share)})
                tot_price = tot_price + math.trunc(i.price-i.price/100*admin_share)
            shop_product.append({'shop' : k , 'orders' : final_orders , 'total' : tot_price })
    delivery = []
    for i in DeliveryAdminShare.objects.all():
        admin_share = int(i.share_percentage)
    for k in DeliveryPerson.objects.all():
        tot_price = int('0')
        person_tasks = []
        for i in DeliveryTasks.objects.all():
            if int(i.person.pk) == int(k.pk):
                for p in Order.objects.all():
                    if str(i.status) == "Completed":
                        if int(i.order.pk) == int(p.pk):
                            if p not in person_tasks:
                                person_tasks.append({'task' : i , 'order' : p , 'price' : math.trunc(i.order.delivery-i.order.delivery/100*admin_share)})
                                tot_price = tot_price + math.trunc(i.order.delivery-i.order.delivery/100*admin_share)
        for g in DeliveryPersonPayment.objects.all():
            for p in person_tasks:
                if int(g.order.pk) == int(p.get('order').pk):
                    person_tasks.remove(p)
        if person_tasks != []:
            delivery.append({'rider' : k , 'task' : person_tasks , 'total' : tot_price})
    context = {
        'shop_product' : shop_product ,
        'delivery' : delivery ,
        'form' : form ,
        'user' : user ,
    }
    return render(request,'accounts/payment/pay.html',context)

def ManageDeliveryAccountView(request):
    user = request.user.groups.values('name')
    unpaid_tasks = []
    paid_tasks = []
    for k in DeliveryTasks.objects.all():
        if int(k.person.user) == int(request.user.pk):
            for i in Order.objects.all():
                if int(k.order.pk) == int(i.pk):
                    if str(i.status) == 'Delivered':
                        for v in DeliveryPersonPayment.objects.all():
                            for t in DeliveryAdminShare.objects.all():
                                admin_share = t.share_percentage
                                break
                            fees = i.delivery-i.delivery/100*admin_share
                            if int(i.pk) == int(v.order.pk):
                                paid_tasks.append({'order' : i , 'fees' : math.trunc(fees) , 'task' : k , 'payment' : v})
                            else:
                                unpaid_tasks.append({'order' : i , 'fees' : math.trunc(fees) , 'task' : k , 'payment' : v})
    context = {
        'unpaid_tasks' : unpaid_tasks ,
        'paid_tasks' : paid_tasks ,
        'user' : user ,
    }
    return render(request,'accounts/delivery.html',context)

def ManageAccountPaymentDetailView(request,order):
    user = request.user.groups.values('name')
    order = get_object_or_404(Order,pk = int(order))
    payment = get_object_or_404(DeliveryPersonPayment,order=order)
    context = {
        'payment' : payment ,
        'user' : user ,
    }
    return render(request,'accounts/payment.html',context)

def ManageAccountShopPaymentView(request,shop):
    user = request.user.groups.values('name')
    shop = get_object_or_404(Shops , pk = shop)
    if request.method == 'POST':
        for i in Order.objects.all():
            for v in request.POST:
                if str(v) == str(i):
                    image = Image.open(request.FILES.getlist('proof'))
                    size = image.size
                    image = image.convert('RGB')
                    rsize = []
                    rsize.append(int(275*1))
                    rsize.append(int(275*(size[0]/size[1])))
                    rimg = image.resize(((rsize[1]),(rsize[0])),Image.ANTIALIAS)
                    img_io = BytesIO()
                    rimg.save(img_io, format='JPEG', quality=75)
                    img_content = ContentFile(img_io.getvalue(),"img.jpg" )
                    form1 = ManagePaymentProofForm({

                    },{
                        'image' : img_content
                    })
                    if form1.is_valid():
                        k = form1.save()
                    form = ManageShopkeperPaymentForm({
                        'order' : i.pk ,
                        'payment' : request.POST.get(v) ,
                        'proof' : k ,
                        'accepted' : 'False' ,
                    })
                    if form.is_valid():
                        form.save()
        context = {
            'user' : user ,
        }
        return render(request,'accounts/payment/shop/paid.html',context)
    else:
        for i in ShopAdminShare.objects.all():
            admin_share = i.share_percentage
            break
        orders = request.GET.getlist('order')
        price = []
        total_price = int('0')
        for i in orders:
            order = get_object_or_404(Order , pk = int(i))
            prices = order.price - order.price/100*admin_share
            price.append({'order' : order , 'price' : math.trunc(prices)})
            total_price = total_price + int(math.trunc(prices))
        form = ManageShopkeperPaymentForm()
        context = {
            'total_price' : total_price ,
            'shop' : shop ,
            'price' : price ,
            'form' : form ,
            'user' : user ,
        }
        return render(request,'accounts/payment/shop/form.html',context)

def ManageAccountDeliveryPaymentView(request,person):
    user = request.user.groups.values('name')
    person = get_object_or_404(DeliveryPerson , pk = person)
    if request.method == 'POST':
        for i in Order.objects.all():
            for v in request.POST:
                if str(v) == str(i):
                    form1 = ManagePaymentProofForm({

                    },{
                        'image' : request.FILES.get('proof')
                    })
                    if form1.is_valid():
                        k = form1.save()
                    form = ManageDeliveryPersonPaymentForm({
                        'order' : i.pk ,
                        'payment' : request.POST.get(v) ,
                        'proof' : k ,
                        'accepted' : 'False' ,
                    })
                    if form.is_valid():
                        form.save()
        context = {
            'user' : user ,
        }
        return render(request,'accounts/payment/shop/paid.html',context)
    else:
        for i in DeliveryAdminShare.objects.all():
            admin_share = i.share_percentage
            break
        orders = request.GET.getlist('order')
        price = []
        total_price = int('0')
        for i in orders:
            order = get_object_or_404(Order , pk = int(i))
            prices = order.price - order.price/100*admin_share
            price.append({'order' : order , 'price' : math.trunc(prices)})
            total_price = total_price + int(math.trunc(prices))
        form = ManageDeliveryPersonPaymentForm()
        context = {
            'total_price' : total_price ,
            'person' : person ,
            'price' : price ,
            'form' : form ,
            'user' : user ,
        }
        return render(request,'accounts/payment/delivery/form.html',context)


