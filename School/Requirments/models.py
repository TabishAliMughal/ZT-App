from django.db import models



class Classes(models.Model):
    code = models.AutoField(primary_key = True)
    serial = models.IntegerField()
    class_name = models.CharField(max_length=200 , unique = True)
    def __str__(self):
        return self.class_name

class Subjects(models.Model):
    code = models.AutoField(primary_key = True)
    subject_name = models.CharField(max_length=200 , unique = True)
    def __str__(self):
        return self.subject_name

class ClassSubjects(models.Model):
    code = models.AutoField(primary_key = True)
    class_name = models.ForeignKey(Classes, on_delete = models.CASCADE)
    subject_name = models.ForeignKey(Subjects, on_delete = models.CASCADE)
    def __str__(self):
        return '{}. {}'.format(str(self.class_name), str(self.subject_name))

class Session(models.Model):
    code = models.AutoField(primary_key = True)
    session_number = models.IntegerField()
    session_start_date = models.DateField()
    def __str__(self):
        return '{}'.format(str(self.session_number))

class Visits(models.Model):
    code = models.AutoField(primary_key = True)
    page = models.CharField(max_length = 50)
    visits = models.IntegerField()
    date = models.DateField()
    def __str__(self):
        return '{}'.format(str(self.page))
    
