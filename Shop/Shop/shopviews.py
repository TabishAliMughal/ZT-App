from App.Creator.models import Creator
from django.shortcuts import render, get_object_or_404 , redirect

from Shop.Customer.models import UserData
from .models import Product , Shops , ProductImages , ProductVideos
from .forms import ManageProductCreateForm , ManageShopCreateForm , ManageUnitCreateForm , ManageProductImageCreateForm , ManageProductVideoCreateForm
from App.Authentication.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from App.Authentication.user_handeling import allowed_users
from Shop.Orders.models import Order , OrderItem
from Shop.Delivery.models import DeliveryPerson 
from datetime import datetime
from django.core.mail import send_mail
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile


@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Admin'])
def ManageShopsListView(request):
    user = request.user.groups.values('name')
    shops = []
    for i in Shops.objects.all():
        shops.append(i)
    context = {
        'user' : user ,
        'shops' : shops ,
    }
    return render(request , 'shop/list.html' , context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Creator'])
def ManageShopCreateView(request):
    user = request.user.groups.values('name')
    if request.method == 'POST':
        data = request.POST
        user1 = get_object_or_404(Creator , user = request.user.pk)
        shop = True
        for i in Shops.objects.all():
            if i.name == data.get('shop_name'):
                shop = False
        if shop == True:
            form = ManageShopCreateForm({
                'name' : data.get('shop_name') ,
                'user' : user1 ,
                'active' : 'False' ,
            })
            form.save()
            # send_mail(
            #     'New Request',
            #     'Here is a new shop owner who wants to join your orgnization.\nHis Shop name is {}\nHis User Name Is {} \nHis Profile Is Not Active Yet \nYou Can Activate His Profile Here : http://zt-app.herokuapp.com/shop/shop/list/for_admin'.format(data.get('shop_name'),user),
            #     'ztapp000@gmail.com' ,
            #     ['tabishalimughal@gmail.com','zahid.a.mughal@gmail.com']
            # )
            context = {
                'user' : user ,
                'return' : 'Your Request Has Been Submited',
            }
            return render(request , 'shop/created.html' , context)
        else:
            context = {
                'user' : user ,
                'return' : 'Another Shop Exist Of This Name Please Try Again',
            }
            return render(request , 'shop/request.html' , context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Admin'])
def ManageShopsEditView(request,shop):
    user = request.user.groups.values('name')
    shop = get_object_or_404(Shops, pk = int(shop))
    lat = ''
    lon = ''
    if request.method == 'POST':
        data = request.POST
        form = ManageShopCreateForm({
            'name' : data.get('name') ,
            'user' : data.get('user') ,
            'address' : str("SRID=4326;"+data.get('address')) ,
            'active' : data.get('active') ,
        } or None , instance=shop)
        form.save()
        return redirect('shop:shop_list')
    else:
        form = ManageShopCreateForm(instance = shop)
        if shop.address:
            lat = shop.address[1]
            lon = shop.address[0]
        context = {
            'user' : user ,
            'form' : form ,
            'lat' : lat ,
            'lon' : lon ,
        }
        return render(request , 'shop/edit.html' , context)

def ManageShopProductListView(request,shop=None):
    user = request.user.groups.values('name')
    sel_shop = None
    if shop == None:
        for i in Shops.objects.all():
            if str(i.user) == str(get_object_or_404(Creator , user = request.user.pk).pk):
                sel_shop = i
    else:
        sel_shop = get_object_or_404(Shops , pk = int(shop))
    if sel_shop != None:
        products = []
        for i in Product.objects.all():
            if str(i.shop.user) == str(sel_shop.user):
                products.append(i)
        final_products = []
        for i in products:
            images = []
            for v in ProductImages.objects.all():
                if int(i.pk) == int(v.product.pk):
                    images.append(v)
                    break
            final_products.append({'product': i , 'image' : images})
        context = {
            'user' : user ,
            'products': final_products ,
            'shop': sel_shop ,
        }
        return render(request,'shop/shopkeeper/list.html',context)
    else:
        context = {
            'user' : user ,
        }
        return render(request,'shop/request.html',context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Creator'])
def ManageShopProductCreateView(request,shop):
    user = request.user.groups.values('name')
    form = {
        'product' : ManageProductCreateForm(),
        'image' : ManageProductImageCreateForm(),
        'video' : ManageProductVideoCreateForm(),
    }
    if request.method == 'POST':
        data = request.POST
        abc = data.get('name')
        slug = ''
        for i in abc:
            if i == ' ':
                slug = 'slug' + '-'
            else:
                slug = 'slug' + str(i)
        form = ManageProductCreateForm({
            'shop': int(shop) ,
            'category': data.get('category') ,
            'name': data.get('name') ,
            'slug': slug.lower() ,
            'description': data.get('description') ,
            'price': data.get('price') ,
            'available': data.get('available') ,
            'unit': data.get('unit') ,
            'condition': data.get('condition') ,
        })
        k = form.save()
        v = int('0')
        for i in request.FILES.getlist('image'):
            image = Image.open(request.FILES.getlist('image')[v])
            size = image.size
            image = image.convert('RGB')
            rsize = []
            rsize.append(int(275*1))
            rsize.append(int(275*(size[0]/size[1])))
            rimg = image.resize(((rsize[1]),(rsize[0])),Image.ANTIALIAS)
            img_io = BytesIO()
            rimg.save(img_io, format='JPEG', quality=75)
            img_content = ContentFile(img_io.getvalue(),"img.jpg" )
            img = ManageProductImageCreateForm({
                'product' : k ,
            },
            {
                'image' : img_content ,
            })
            v = v + 1
            img.save()
        v = int('0')
        for i in request.FILES.getlist('video'):
            vid = ManageProductVideoCreateForm({
                'product' : k ,
            },
            {
                'video' : request.FILES.getlist('video')[v] ,
            })
            v = v + 1
            vid.save()
        return redirect('shop:shop_products')
    else:
        context = {
            'user' : user ,
            'form': form ,
        }
        return render(request,'shop/shopkeeper/create.html',context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Creator'])
def ManageShopProductEditView(request,product):
    user = request.user.groups.values('name')
    product = get_object_or_404(Product, pk = int(product))
    form = {
        'product' : ManageProductCreateForm(instance=product),
    }
    if request.method == 'POST':
        data = request.POST
        slug = ''
        for i in data.get('name'):
            if i == ' ':
                slug = slug + '-'
            else:
                slug = slug + i
        form = ManageProductCreateForm({
            'shop': int(product.shop.pk) ,
            'category': data.get('category') ,
            'name': data.get('name') ,
            'slug': slug.lower() ,
            'description': data.get('description') ,
            'price': data.get('price') ,
            'available': data.get('available') ,
            'unit': data.get('unit') ,
            'condition': data.get('condition') ,
        }, instance=product)
        k = form.save()
        v = int('0')
        for i in request.FILES.getlist('image'):
            image = Image.open(request.FILES.getlist('image')[v])
            size = image.size
            image = image.convert('RGB')
            rsize = []
            rsize.append(int(275*1))
            rsize.append(int(275*(size[0]/size[1])))
            rimg = image.resize(((rsize[1]),(rsize[0])),Image.ANTIALIAS)
            img_io = BytesIO()
            rimg.save(img_io, format='JPEG', quality=75)
            img_content = ContentFile(img_io.getvalue(),"img.jpg" )
            img = ManageProductImageCreateForm({
                'product' : k ,
            },
            {
                'image' : img_content ,
            })
            v = v + 1
            img.save()
        v = int('0')
        for i in request.FILES.getlist('video'):
            vid = ManageProductVideoCreateForm({
                'product' : k ,
            },
            {
                'video' : request.FILES.getlist('video')[v] ,
            })
            v = v + 1
            vid.save()
        return redirect('shop:shop_products')
    else:
        images = []
        for i in ProductImages.objects.all():
            if int(i.product.pk) == int(product.pk):
                images.append(i)
        videos = []
        for i in ProductVideos.objects.all():
            if int(i.product.pk) == int(product.pk):
                videos.append(i)
        context = {
            'user' : user ,
            'form': form ,
            'name': product.name ,
            'description': product.description ,
            'price': product.price ,
            'images': images ,
            'videos': videos ,
        }
        return render(request,'shop/shopkeeper/create.html',context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Creator'])
def ManageShopProductSoldView(request,product):
    product = get_object_or_404(Product, pk = int(product))
    form = ManageProductCreateForm({
        'shop': product.shop ,
        'category': product.category ,
        'name': product.name ,
        'slug': product.slug ,
        'description': product.description ,
        'price': product.price ,
        'available': 'False' ,
        'unit': product.unit ,
        'condition': product.condition ,
    },instance=product)
    form.save()
    return redirect('shop:shop_products')

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Creator'])
def ManageShopProductPictureDeleteView(request,picture):
    picture = get_object_or_404(ProductImages, pk = int(picture))
    product = picture.product.pk
    picture.delete()
    return redirect('shop:shop_product_edit',product)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Creator'])
def ManageShopProductVideoDeleteView(request,video):
    video = get_object_or_404(ProductVideos, pk = int(video))
    product = video.product.pk
    video.delete()
    return redirect('shop:shop_product_edit',product)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Creator'])
def ManageShopOrdersListView(request):
    user = request.user.groups.values('name')
    shop = ''
    for i in Shops.objects.all():
        if int(i.user) == int(get_object_or_404(Creator,user = request.user.pk).pk):
            shop = i
    orders = []
    for v in Order.objects.all():
        products = []
        for i in OrderItem.objects.all():
            if str(i.product.shop.pk) == str(shop.pk):
                    if str(v.pk) == str(i.order.pk):
                        products.append({'product':i.product , 'qty':i.quantity})
        orders.append({'pk' : v.pk , 'products': products , 'status' : v.status})
    j = int('0')
    for k in orders:
        if k.get('products') == []:
            j = j + 1
    for h in range(0,j):
        for k in orders:
            if k.get('products') == []:
                orders.remove(k)
    context = {
        'orders': orders ,
        'user' : user ,
        'shop' : shop ,
    }
    return render(request,'shop/shopkeeper/Orders/list.html',context)

@login_required(login_url='main_login')
@allowed_users(allowed_roles=['Creator'])
def ManageShopOrderDetailView(request,order):
    user = request.user.groups.values('name')
    shop = ''
    for i in Shops.objects.all():
        if int(i.user) == int(get_object_or_404(Creator,user = request.user.pk).pk):
            shop = i
    order = get_object_or_404(Order , pk = int(order) )
    products = []
    for i in OrderItem.objects.all():
        if str(order.pk) == str(i.order.pk):
            if str(i.product.shop.pk) == str(shop.pk):
                products.append({'product':i.product , 'qty':i.quantity , 'price': i.price , 'date' : order.created})
    total = int('0')
    for i in products:
        price = i['price']
        total = total + price
    delivery = []
    if str(order.status) == 'Pending':
        for i in DeliveryPerson.objects.all():
            now = datetime.now().time()
            if str(now) > str(i.start_time) and str(now) < str(i.end_time):
                if str(i.active) == "Active":
                    delivery.append(i)
    context = {
        'shop' : shop ,
        'delivery' : delivery ,
        'products' : products ,
        'total': total ,
        'order': order ,
        'user' : user ,
    }
    return render(request,'shop/shopkeeper/Orders/detail.html',context)

def ManageProductUnitsAdd(request):
    if request.method == 'POST':
        unitform = ManageUnitCreateForm({
            'name': request.POST.get('name')
        })
        if unitform.is_valid:
            unitform.save()
        return redirect('shop:shop_products')
    else:
        form = ManageUnitCreateForm()
        context = {
            'form':form,
        }
        return render(request,'shop/shopkeeper/unitcreate.html',context)