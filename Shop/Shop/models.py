from django.contrib.gis.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from Creator.models import Creator


class Units(models.Model):
    name = models.CharField(max_length = 25)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Units'

class Shops(models.Model):
    name = models.CharField(max_length=200)
    # user = models.ForeignKey(Creator,on_delete=models.CASCADE)
    user = models.IntegerField()
    address = models.PointField(geography=True, default='POINT(0.0 0.0)')
    active = models.BooleanField()
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Shops'

class Category(models.Model):
    name = models.CharField(max_length=200,db_index=True)
    slug = models.SlugField(max_length=200)
    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',args=[self.slug])
    class Meta:
        verbose_name_plural = 'Categories'

class Product(models.Model):
    shop = models.ForeignKey(Shops,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,related_name='products',on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    unit = models.ForeignKey(Units , on_delete=models.CASCADE)
    condition = models.CharField(choices = [('New' , 'new') , ('Old' , 'old')] , max_length=4)
    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('shop:product_detail',args=[self.id, self.slug])
    class Meta:
        verbose_name_plural = 'Products'

class ProductImages(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    class Meta:
        verbose_name_plural = 'Product Images'

class ProductVideos(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    video = models.FileField(upload_to='products/')
    class Meta:
        verbose_name_plural = 'Product Videos'