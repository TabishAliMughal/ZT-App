from django import forms
from .models import ShopkeperPayment , DeliveryPersonPayment , PaymentProof

class ManageShopkeperPaymentForm(forms.ModelForm):
    class Meta:
        model = ShopkeperPayment
        fields = [
            'order' ,
            'payment' ,
            'proof' ,
            'accepted' ,
        ]

class ManageDeliveryPersonPaymentForm(forms.ModelForm):
    class Meta:
        model = DeliveryPersonPayment
        fields = [
            'order' ,
            'payment' ,
            'proof' ,
            'accepted' ,
        ]
        
class ManagePaymentProofForm(forms.ModelForm):
    class Meta:
        model = PaymentProof
        fields = [
            'image' ,
        ]
