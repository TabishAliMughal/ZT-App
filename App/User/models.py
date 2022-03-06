from django.contrib.gis.db import models
from django.contrib.auth.models import User



class Creator(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    mobile = models.CharField(max_length=11)
    nic = models.CharField(max_length=15,blank=True)
    bank_account = models.CharField(max_length=24 , blank=True)
    easypaisa = models.CharField(max_length=11 , blank=True)
    def __str__(self):
        return self.name
    class Meta:
        app_label = 'Creator'

class UserData(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    picture = models.ImageField(blank = True , null = True , upload_to = 'user/profile')
    first_name = models.CharField(max_length=250)
    address = models.PointField(blank=True,null=True)
    city = models.CharField(blank=True,null=True,max_length=250)
    mobile = models.CharField(blank=True,null=True,max_length=11)
    nic = models.CharField(max_length=15,blank=True)
    bank_account = models.CharField(max_length=24 , blank=True)
    easypaisa = models.CharField(max_length=11 , blank=True)
    def __str__(self):
        return self.first_name
    class Meta:
        verbose_name_plural = 'Users'