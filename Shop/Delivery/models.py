from django.contrib.gis.db import models
from django.contrib.auth.models import User
from Shop.Orders.models import Order , OrderItem
from Shop.Shop.models import Shops
from Shop.Customer.models import UserData
from django.contrib.gis.geos import Point


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
    area = models.PointField(geography=True, spatial_index=True,default=(Point(0.0, 0.0, srid=4326)))
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Delivery Person'

class DeliveryTasks(models.Model):
    person = models.ForeignKey(DeliveryPerson , on_delete=models.CASCADE)
    order = models.ForeignKey(Order , on_delete=models.CASCADE)
    task_from = models.ForeignKey(Shops,on_delete=models.CASCADE)
    task_to = models.ForeignKey(UserData,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    pick = models.DateTimeField(blank=True,null=True)
    drop = models.DateTimeField(blank=True,null=True)
    status = models.CharField(max_length=50)
    class Meta:
        verbose_name_plural = 'Delivery Task'
    def pick_time(self):
        if str(self.pick) != 'None':
            return self.pick.strftime('%d-%m-%Y,%H:%M:%S')
        else:
            return "Not Picked Yet"
    def drop_time(self):
        if str(self.drop) != 'None':
            return self.drop.strftime('%d-%m-%Y,%H:%M:%S')
        else:
            return "Not Droped Yet"


class DeliveryProof(models.Model):
    order = models.ForeignKey(Order , on_delete=models.CASCADE)
    image = models.ImageField(upload_to="shop/delivery_proof")
    date = models.DateField(auto_now_add=True)
    class Meta:
        verbose_name_plural = 'Delivery Proof'
