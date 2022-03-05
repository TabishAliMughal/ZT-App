from django.db import models


class TeacherVisit(models.Model):
    code = models.AutoField(primary_key = True , unique = True)
    name = models.CharField(max_length = 50)
    phone = models.CharField(max_length = 11)
    email = models.EmailField(blank = True , null = True)
    seen = models.BooleanField()
    def __str__(self):
        return self.name


class SchoolVisit(models.Model):
    code = models.AutoField(primary_key = True , unique = True)
    name = models.CharField(max_length = 50)
    school_name = models.CharField(max_length = 50)
    phone = models.CharField(max_length = 11)
    email = models.EmailField(blank = True , null = True)
    seen = models.BooleanField()
    def __str__(self):
        return self.name


class ParentVisit(models.Model):
    code = models.AutoField(primary_key = True , unique = True)
    name = models.CharField(max_length = 50)
    student_name = models.CharField(max_length = 50)
    phone = models.CharField(max_length = 11)
    email = models.EmailField(blank = True , null = True)
    seen = models.BooleanField()
    def __str__(self):
        return self.name