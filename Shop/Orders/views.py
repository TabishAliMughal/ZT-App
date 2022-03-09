from django.shortcuts import render , get_object_or_404 , redirect
from .models import OrderItem , Order, OrderReview
from .forms import OrderCreateForm , OrderItemsCreateForm, OrderReviewForm
from App.User.models import UserData
from Shop.Cart.cart import Cart
from Shop.Shop.models import Product , Shops
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group , User
from App.Authentication.user_handeling import unauthenticated_user, allowed_users, admin_only
from Shop.Cart.calculations import LatLonCalculator
from Shop.Cart.models import DeliveryCharge
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile



@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Shop_Public'])
def ManageOrderCreateView(request,user):
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
                if int(u.user.pk) == int(request.user.pk):
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
                    'user' : curr_user.pk ,
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
            return render(request,'Orders/Order/Created.html',context)
        else:
            return render(request,'error.html',{'return' : 'Plese Select Some Items'})
    else:
        user = []
        for i in UserData.objects.all():
            if int(i.user.pk) == int(request.user.pk):
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
        return render(request,'Orders/Order/Create.html',context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Shop_Creator'])
def ManageDeliveryPersonCallView(request):
    if request.method == 'POST':
        data = request.POST
        order = get_object_or_404(Order , pk = data.get('order'))
        Order.objects.filter(pk = order.pk).update(status = 'DeliveryCalled')
        return redirect('shop:shop_orders')

def ManageOrderReview(request,order):
    order = get_object_or_404(Order , pk = order)
    try:
        review = get_object_or_404(OrderReview , order = order)
    except:
        review = None
    if request.method == 'POST':
        if request.FILES.get('image'):
            image = Image.open(request.FILES.get('image'))
            size = image.size
            image = image.convert('RGB')
            rsize = []
            rsize.append(int(275*1))
            rsize.append(int(275*(size[0]/size[1])))
            rimg = image.resize(((rsize[1]),(rsize[0])),Image.ANTIALIAS)
            img_io = BytesIO()
            rimg.save(img_io, format='JPEG', quality=75)
            img_content = ContentFile(img_io.getvalue(),"img.jpg" )
        else:
            img_content = request.FILES.get('image')
        if review:
            form = OrderReviewForm({
                'order': request.POST.get('order') or review.order ,
                'text': request.POST.get('text') or review.text or None ,
                'stars': request.POST.get('stars') or review.stars ,
            } or None , { 'image' : img_content} or None , instance=review)
        else:
            form = OrderReviewForm({
                'order': request.POST.get('order') ,
                'text': request.POST.get('text') or None ,
                'stars': request.POST.get('stars') ,
            } or None , { 'image' : img_content})
        form.save()
        return redirect('shop_costumer:previous_orders')
    else:
        form = OrderReviewForm(instance=review)
        context = {
            'review':review,
            'order':order,
            'form':form,
        }
        return render(request,'Orders/Order/Review.html',context)
