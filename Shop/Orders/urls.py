from django.urls import path 
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/<user>', views.ManageOrderCreateView, name='order_create'),
    path('packed/', views.ManageDeliveryPersonCallView, name='call_for_delivery'),
    path('order/review/<order>', views.ManageOrderReview, name='order_review'),
]