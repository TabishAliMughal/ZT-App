from django.contrib.gis.db import models
from django.contrib.auth.models import User

class UserData(models.Model):
    # user = models.ForeignKey(User,on_delete=models.CASCADE)
    user = models.IntegerField()
    first_name = models.CharField(max_length=250)
    address = models.PointField()
    city = models.CharField(max_length=250)
    def __str__(self):
        return self.first_name
    class Meta:
        verbose_name_plural = 'Customers'