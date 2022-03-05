from django.db import models
from School.Requirments.models import *
from django.contrib.auth.models import User
from School.RegSchool.models import *


class Indivisuals(models.Model):
    code = models.AutoField(primary_key = True , unique = True)
    start_date = models.DateField()
    # user = models.ForeignKey(User , on_delete = models.CASCADE)
    user = models.IntegerField()
    name = models.CharField(max_length = 50)
    father_name = models.CharField(max_length = 50)
    school = models.ForeignKey(School , on_delete = models.CASCADE , blank = True , null = True)
    mobile = models.CharField(max_length = 50)
    clas = models.ForeignKey(Classes , on_delete = models.CASCADE)
    fees = models.IntegerField()
    password = models.CharField(max_length = 50)
    active = models.BooleanField()
    def __str__(self):
        return self.name

