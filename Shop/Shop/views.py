from django.shortcuts import render, get_object_or_404 , HttpResponse
from .models import Category, Product , Shops , ProductImages , ProductVideos
from .forms import *
from Shop.Cart.forms import CartAddProductForm
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
import geocoder
from Creator.models import Creator
from django.template import loader


def ManageProductListView(request, category_slug=None , shop=None , product_type=None):
    user = request.user.groups.values('name')
    shopcreateform = ManageShopCreateForm()
    category = None
    categories = Category.objects.all()
    if product_type != None or category_slug != None:
        location = []
        try:
            g = geocoder.ip('me')
            loc = g.latlng
        except:
            loc = 'None'
        if str(loc) == 'None':
            selshop = Shops.objects.all()
        else:
            for i in loc:
                location.append(i)
            latitude = location[0]
            longitude = location[1]
            user_location = Point(longitude, latitude, srid=4326)
            selshop = Shops.objects.annotate(distance=Distance('address',user_location)).order_by('distance')
        products = []
        for i in selshop:
            for d in Shops.objects.all().filter(pk = i.pk,active = 'True'):
                selshop = ''
                if shop:
                    products = Product.objects.all().filter(shop = get_object_or_404(Shops , pk = shop))
                if category_slug:
                    if product_type != None:
                        products = Product.objects.all().filter(category = get_object_or_404(Category , slug = category_slug),condition = product_type)
                    else:
                        products = Product.objects.all().filter(category = get_object_or_404(Category , slug = category_slug))
                if not shop and not category_slug:
                    products = Product.objects.all().filter(shop = i , available = 'True')
        # for i in selshop:
        #     for d in Shops.objects.all():
        #         if str(i.pk) == str(d.pk):
        #             if str(d.active) == str(True):
                        # for v in Product.objects.all():
                        #     selshop = ''
                        #     if shop:
                        #         if str(shop) == str(v.shop.pk):
                        #             if v not in products:
                        #                 products.append(v)
                        #                 selshop = get_object_or_404(Shops , pk = int(shop) )
                        #     if category_slug:
                        #         if str(category_slug) == str(v.category.slug):
                        #             if product_type != None:
                        #                 if str(v.condition) == str(product_type):
                        #                     if v not in products:
                        #                         products.append(v)
                        #                         category = get_object_or_404(Category, slug = category_slug)
                        #             else:
                        #                 if v not in products:
                        #                     products.append(v)
                        #                     category = get_object_or_404(Category, slug = category_slug)
                        #     if not shop and not category_slug:
                        #         if str(i.pk) == str(v.shop.pk):
                        #             if str(v.available) == 'True':
                        #                 if v not in products:
                        #                     products.append(v)
        final_products = []
        for i in products:
            images = []
            for v in ProductImages.objects.all():
                if int(i.pk) == int(v.product.pk):
                    images.append(v)
                    break
            final_products.append({'product': i , 'image' : images})
        context = {
            'request': request ,
            'shopcreateform': shopcreateform ,
            'user' : user,
            'category': category,
            'categories': categories,
            'products': final_products,
            'shop': selshop,
            'all' : 'Selected',
            }
        return render(request,'shop/product/list.html',context)
    else :
        all_products = []
        for i in Category.objects.all():
            new_product = []
            old_product = []
            for v in Product.objects.all():
                if int(i.pk) == int(v.category.pk):
                    if v.condition == 'New':
                        if str(len(new_product)) <= '5':
                            new_product.append(v)
                    if v.condition == 'Old':
                        if str(len(old_product)) <= '5':
                            old_product.append(v)
            if new_product != []:
                prod = []
                for i in new_product:
                    images = []
                    for v in ProductImages.objects.all():
                        if int(i.pk) == int(v.product.pk):
                            images.append(v.image.url)
                            break
                    prod.append({'product':i , 'image': images})
                all_products.append({'category' : i.category , 'products' : prod , 'type' : 'New' })
            if old_product != []:
                prod = []
                for i in old_product:
                    images = []
                    for v in ProductImages.objects.all():
                        if int(i.pk) == int(v.product.pk):
                            images.append(v.image.url)
                            break
                    prod.append({'product':i , 'image': images})
                all_products.append({'category' : i.category , 'products' : prod , 'type' : 'Old' })
        context = {
            'shopcreateform': shopcreateform ,
            'all_products' : all_products ,
            'user' : user ,
            'all' : 'all' ,
            'categories' : categories ,
        }
        return render(request,'shop/product/list.html',context)

def ManageProductDetailView(request, id, slug):
    user = request.user.groups.values('name')
    product = []
    for v in Product.objects.all():
        if str(v.pk) == str(id) and str(v.slug) == str(slug) and str(v.available) == 'True':
            k = int('0')
            videos = []
            for l in ProductVideos.objects.all():
                if int(v.pk) == int(l.product.pk):
                    k = k + 1
                    videos.append({ "video" : l.video.url,'count':k})
            images = []
            for l in ProductImages.objects.all():
                if int(v.pk) == int(l.product.pk):
                    k = k + 1
                    images.append({ "image" : l.image.url,'count':k})
            product = {'product': v , 'image' : images , 'video' : videos , 'total' : k}
    cart_product_form = CartAddProductForm()
    context = {
        'user' : user,
        'product': product,
        'cart_product_form': cart_product_form
        }
    return render(request,'shop/product/detail.html',context)
