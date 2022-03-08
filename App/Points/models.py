from django.db import models
from App.User.models import UserData

class Points(models.Model):
    user = models.ForeignKey(UserData , on_delete=models.CASCADE )
    points = models.IntegerField()