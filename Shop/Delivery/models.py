from django.contrib.gis.db import models
from django.contrib.auth.models import User
from Shop.Orders.models import Order , OrderItem
from Shop.Shop.models import Shops
from Shop.Customer.models import UserData


class DeliveryPerson(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.IntegerField()
    name = models.CharField(max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()
    active = models.CharField(max_length=50)
    mobile = models.CharField(max_length=11)
    nic = models.CharField(max_length=15)
    bank_account = models.CharField(max_length=24 , blank=True)
    easypaisa = models.CharField(max_length=11 , blank=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Delivery Person'

class DeliveryTasks(models.Model):
    person = models.ForeignKey(DeliveryPerson , on_delete=models.CASCADE)
    order = models.ForeignKey(Order , on_delete=models.CASCADE)
    task_from = models.ForeignKey(Shops,on_delete=models.CASCADE)
    task_to = models.ForeignKey(UserData,on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=50)
    class Meta:
        verbose_name_plural = 'Delivery Task'

class DeliveryProof(models.Model):
    order = models.ForeignKey(Order , on_delete=models.CASCADE)
    image = models.ImageField(upload_to="shop/delivery_proof")
    date = models.DateField(auto_now_add=True)
    class Meta:
        verbose_name_plural = 'Delivery Proof'



