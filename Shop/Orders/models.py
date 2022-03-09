from django.contrib.gis.db import models
from Shop.Shop.models import Product
from App.User.models import UserData
from django.contrib.auth.models import User


class Order(models.Model):
    # user = models.ForeignKey(UserData,on_delete=models.CASCADE)
    user = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    status = models.CharField(max_length=250)
    price = models.IntegerField()
    delivery = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ('-created',)
    def __str__(self):
        return 'Order {}'.format(self.id)
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
    class Meta:
        verbose_name_plural = 'Orders'

class OrderItem(models.Model):
    order = models.ForeignKey(Order,related_name='items',on_delete=models.CASCADE)
    product = models.ForeignKey(Product,related_name='order_items',on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    def __str__(self):
        return '{}'.format(self.id)
    def get_cost(self):
        return self.price * self.quantity
    class Meta:
        verbose_name_plural = 'Order Items'

class OrderReview(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    text = models.CharField(max_length=500,blank=True,null=True)
    image = models.FileField(blank=True,null=True)
    stars = models.IntegerField(default=0)
    def __str__(self):
        return '{}'.format(self.order)
    class Meta:
        verbose_name_plural = 'Order Reviews'

