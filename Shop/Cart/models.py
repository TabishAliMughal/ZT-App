from django.contrib.gis.db import models

# Create your models here.
class DeliveryCharge(models.Model):
    compulsory = models.IntegerField()
    per_km = models.IntegerField()
    class Meta:
        verbose_name_plural = 'Delivery Charge'