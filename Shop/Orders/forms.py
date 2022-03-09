from django import forms
from .models import Order , OrderItem, OrderReview


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


class OrderReviewForm(forms.ModelForm):
    class Meta:
        model = OrderReview
        fields = [
            'order',
            'text',
            'image',
            'stars',
        ]