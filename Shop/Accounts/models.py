from django.db import models
from Shop.Orders.models import Order

class PaymentProof(models.Model):
    image = models.ImageField(upload_to='accounts/payment_proof' )
    class Meta:
        verbose_name_plural = 'Payment Proof'

class ShopkeperPayment(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    payment = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    proof = models.ForeignKey(PaymentProof,on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    class Meta:
        verbose_name_plural = 'Shopkeeper Payment'

class ShopAdminShare(models.Model):
    share_percentage = models.IntegerField()
    class Meta:
        verbose_name_plural = 'Shop Admin Share'

class DeliveryPersonPayment(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    payment = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    proof = models.ForeignKey(PaymentProof,on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    class Meta:
        verbose_name_plural = 'Delivery Person Payment'

class DeliveryAdminShare(models.Model):
    share_percentage = models.IntegerField()
    class Meta:
        verbose_name_plural = 'Delivery Admin Share'
