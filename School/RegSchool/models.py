from django.db import models
from django.contrib.auth.models import User


class School(models.Model):
    code = models.AutoField(primary_key = True)
    school = models.CharField(max_length=150)
    address = models.CharField(max_length=150)
    # user = models.ForeignKey(User,on_delete = models.CASCADE)
    user = models.IntegerField()
    def __str__(self):
        return self.school

