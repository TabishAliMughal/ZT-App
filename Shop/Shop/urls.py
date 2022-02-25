from django.urls import path
from . import views
from . import shopviews

app_name = 'Shop'

urlpatterns = [
    path('', views.ManageProductListView, name='product_list'),
    path('myshop/<shop>', views.ManageProductListView, name='shop_product_list'),
    path('myshop/<shop>/<slug:category_slug>/', views.ManageProductListView,name='shop_product_list_by_category'),
    path('myshop/<category_slug>/<product_type>', views.ManageProductListView,name='shop_product_list_by_category_and_type'),
    path('products/<slug:category_slug>/', views.ManageProductListView,name='product_list_by_category'),
    path('product/<int:id>/<slug:slug>/', views.ManageProductDetailView,name='product_detail'),



    path('shop/list/for_admin', shopviews.ManageShopsListView,name='shop_list'),
    path('shop/edit/<shop>', shopviews.ManageShopsEditView,name='shop_edit'),
    path('shop/register', shopviews.ManageShopCreateView,name='shop_create'),
    path('shop/products', shopviews.ManageShopProductListView, name='shop_products'),
    path('shop/products/<shop>', shopviews.ManageShopProductListView, name='shop_products'),
    path('shop/product/create/<shop>', shopviews.ManageShopProductCreateView, name='shop_product_create'),
    path('shop/product/edit/<product>', shopviews.ManageShopProductEditView, name='shop_product_edit'),
    path('shop/products/delete/<product>', shopviews.ManageShopProductSoldView, name='shop_product_sold'),
    path('shop/products/delete/picture/<picture>', shopviews.ManageShopProductPictureDeleteView, name='shop_product_picture_delete'),
    path('shop/products/delete/video/<video>', shopviews.ManageShopProductVideoDeleteView, name='shop_product_video_delete'),


    path('shop/orders', shopviews.ManageShopOrdersListView, name='shop_orders'),
    path('shop/order/detail/<order>', shopviews.ManageShopOrderDetailView, name='shop_order_detail'),

    path('products/units/add', shopviews.ManageProductUnitsAdd, name='units_add'),

]