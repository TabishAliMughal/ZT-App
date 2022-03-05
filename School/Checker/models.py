from django.db import models
from django.contrib.auth.models import User
from School.Requirments.models import *
from School.Teacher.models import *
from School.Exam.models import *


class CheckerClass(models.Model):
    id = models.AutoField(primary_key = True , unique = True)
    # checker = models.ForeignKey(User , on_delete = models.CASCADE)
    checker = models.IntegerField()
    subject = models.ForeignKey(ClassSubjects , on_delete = models.CASCADE)
    def __str__(self):
        return 'Checker {} of {}'.format(self.checker,self.subject)

