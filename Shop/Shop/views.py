from django.shortcuts import render, get_object_or_404 , HttpResponse

from Shop.Orders.models import Order, OrderItem, OrderReview
from .models import Category, Product , Shops , ProductImages , ProductVideos
from .forms import *
from Shop.Cart.forms import CartAddProductForm
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
import geocoder
from App.User.models import Creator, UserData
from django.template import loader


def ManageProductListView(request, category_slug=None , shop=None , product_type=None):
    shopcreateform = ManageShopCreateForm()
    category = None
    categories = Category.objects.all()
    products = []
    def get_review(i):
        review = []
        reviews = []
        for l in [k.order.pk for k in OrderItem.objects.all().filter(product = i)]:
            for d in OrderReview.objects.all().filter(order = l):
                reviews.append(d.stars)
        total = len(reviews)
        try:
            average = [f for f in range(0,int(sum(reviews) / len(reviews)))]
        except:
            average = None
        review.append({'total':total , 'average':average})
        return review
    def get_images(i):
        images = []
        for v in ProductImages.objects.all():
            if int(i.pk) == int(v.product.pk):
                images.append(v.image.url)
                break
        return images
    if product_type != None or category_slug != None or shop != None:
        location = []
        if shop == None:
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
        else:
            selshop = Shops.objects.all().filter(pk = shop)
        for i in selshop:
            for d in Shops.objects.all().filter(pk = i.pk,active = 'True'):
                if shop:
                    products = Product.objects.all().filter(shop = get_object_or_404(Shops , pk = shop))
                    selshop = get_object_or_404(Shops , pk = shop)
                if category_slug:
                    if product_type != None:
                        products = Product.objects.all().filter(category = get_object_or_404(Category , slug = category_slug),condition = product_type)
                        category = get_object_or_404(Category , slug = category_slug)
                    else:
                        products = Product.objects.all().filter(category = get_object_or_404(Category , slug = category_slug))
                        category = get_object_or_404(Category , slug = category_slug)
                if not shop and not category_slug:
                    products = Product.objects.all().filter(shop = i , available = 'True')
        final_products = []
        for i in products:
            if str(i.available) == 'True':
                images = get_images(i)
                review = get_review(i)
                final_products.append({'product': i , 'image' : images , 'review' : review })
        context = {
            'request': request ,
            'shopcreateform': shopcreateform ,
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
                if str(v.available) == 'True':
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
                    images = get_images(i)
                    review = get_review(i)
                    prod.append({'product':i , 'image': images , 'review' : review})
                all_products.append({'category' : i.category , 'products' : prod , 'type' : 'New' })
            if old_product != []:
                prod = []
                for i in old_product:
                    images = get_images(i)
                    review = get_review(i)
                    prod.append({'product':i , 'image': images , 'review' : review})
                all_products.append({'category' : i.category , 'products' : prod , 'type' : 'Old' })
        context = {
            'shopcreateform': shopcreateform ,
            'all_products' : all_products ,
            'all' : 'all' ,
            'categories' : categories ,
        }
        return render(request,'shop/product/list.html',context)

def ManageProductDetailView(request, id, slug):
    product = []
    for v in Product.objects.all().filter(pk = id , slug = slug , available = 'True'):
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
        reviews = []
        for k in OrderItem.objects.all().filter(product = v):
            for i in OrderReview.objects.all().filter(order = k.order):
                i.user = get_object_or_404(UserData , pk = i.order.user)
                i.stars = [k for k in range(0,i.stars)]
                reviews.append(i)
        product = {'product': v , 'image' : images , 'video' : videos , 'total' : k , 'reviews' : reviews}
    cart_product_form = CartAddProductForm()
    context = {
        'product': product,
        'cart_product_form': cart_product_form
        }
    return render(request,'shop/product/detail.html',context)
