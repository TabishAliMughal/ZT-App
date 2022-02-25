from django.urls import path 
from . import views

app_name = 'costumer'

urlpatterns = [
    path('my_orders/', views.ManagePreviousOrderView, name='previous_orders'),
    path('my_data', views.ManageCostumerDataView, name='costumer_data'),
]