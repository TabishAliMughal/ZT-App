from django.urls import path
from . import views

app_name = 'Accounts'

urlpatterns = [
    path('shop/', views.ManageShopAccountView, name='shop_account'),
    path('delivery/', views.ManageDeliveryAccountView, name='delivery_account'),
    path('payment/<order>', views.ManageAccountPaymentDetailView, name='payment_detail'),
    path('shop/pay/<shop>', views.ManageAccountShopPaymentView, name='shop_pay'),
    path('delivery/pay/<person>', views.ManageAccountDeliveryPaymentView, name='delivery_pay'),
    path('list/', views.ManageShopAccountPaymentListView, name='accounts_list'),
    path('list/pay', views.ManageShopAccountPaymentPayView, name='accounts_pay'),
]