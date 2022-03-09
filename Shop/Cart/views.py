from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from Shop.Shop.models import Product , Shops , ProductImages
from App.User.models import UserData
from .cart import Cart
from .forms import CartAddProductForm
from .calculations import LatLonCalculator
from .models import DeliveryCharge
from django.contrib.auth.decorators import login_required
from App.Authentication.user_handeling import allowed_users


@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Shop_Public'])
def ManageCartDetailView(request):
    unorder_cart = Cart(request)
    for item in unorder_cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],'update': True})
    cart = []
    total_delivery = int('0')
    for i in Shops.objects.all():
        delivery = int('0')
        pro = []
        for v in unorder_cart:
            q = (v.get('update_quantity_form'))
            k = (v.get('total_price'))
            p = (v.get('product'))
            img = ''
            if int(i.pk) == int(p.shop.pk):
                for d in ProductImages.objects.all():
                    if int(p.pk) == int(d.product.pk):
                        img = d.image.url
                        break
                pro.append({ 'product' : p , 'total_price' : k ,'form' : q , 'img' : img })
        if pro != []:
            for u in UserData.objects.all():
                if int(u.user.pk) == int(request.user.pk):
                    t = LatLonCalculator(u.address,i.address)
                    for j in DeliveryCharge.objects.all():
                        delivery = int(j.compulsory) + (int(j.per_km)*int(t))
                        total_delivery = total_delivery + delivery
                        break
            cart.append({'shop': i , 'item' : pro , 'delivery' : delivery})
    context = {
        'cart': cart,
        'u_cart' : unorder_cart ,
        'delivery' : total_delivery,
    }
    return render(request, 'cart/detail.html',context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Shop_Public'])
def ManageCartAddItemView(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,quantity=cd['quantity'],update_quantity=cd['update'])
    return redirect('cart:cart_detail')

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Shop_Public'])
def ManageCartRemoveItemView(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')
