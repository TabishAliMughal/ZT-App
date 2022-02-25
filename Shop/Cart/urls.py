from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.ManageCartDetailView, name='cart_detail'),
    path('add/<int:product_id>/',views.ManageCartAddItemView,name='cart_add'),
    path('remove/<int:product_id>/',views.ManageCartRemoveItemView,name='cart_remove'),
]