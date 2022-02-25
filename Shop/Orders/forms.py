from django import forms
from .models import Order , OrderItem
class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'user',
            'paid',
            'status',
            'price',
            'delivery',
        ]

class OrderItemsCreateForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = [
            'order',
            'product',
            'price',
            'quantity',
        ]