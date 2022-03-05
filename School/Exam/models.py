from django.db import models
from School.Requirments.models import *
from School.Teacher.models import *
from School.Indivisuals.models import *
from django.contrib.contenttypes import fields



class ExamStatus(models.Model):
    code = models.AutoField(primary_key = True)
    exam_number = models.IntegerField()
    class_name = models.ForeignKey(Classes, on_delete = models.CASCADE)
    subject = models.ForeignKey(Subjects ,on_delete=models.CASCADE)
    session = models.ForeignKey(Session ,on_delete=models.CASCADE)
    status = models.BooleanField()
    def __str__(self):
        return 'Exam of {} Class {} and Session {}'.format(self.subject,self.class_name,self.session)

class ExamQuestions(models.Model):
    code = models.AutoField(primary_key = True)
    exam = models.ForeignKey(ExamStatus , on_delete = models.CASCADE)
    question = models.CharField(max_length = 250, blank = True)
    marks = models.IntegerField(blank = True)
    def __str__(self):
        return 'Question Of Class {} Session {}'.format(self.exam.class_name,self.exam.session)

class ExamAnswers(models.Model):
    code = models.AutoField(primary_key=True)
    indi_student = models.ForeignKey(Indivisuals , on_delete=models.CASCADE , null=True , blank=True)
    teach_student = models.ForeignKey(TeacherClassStudents , on_delete=models.CASCADE , null=True , blank=True)
    exam = models.ForeignKey(ExamStatus , on_delete = models.CASCADE)
    picture = models.ImageField(upload_to='exam/papers/answers/' )
    # checker = models.ForeignKey(User , on_delete=models.CASCADE,blank=True,null=True)
    checker = models.IntegerField()
    checked = models.CharField(max_length=8)
    def __str__(self):
        if str(self.indi_student) == 'None':
            return 'Answer Of {}'.format(self.teach_student)
        else:
            return 'Answer Of {}'.format(self.indi_student)

class QuestionsChecked(models.Model):
    code = models.AutoField(primary_key=True)
    # checker = models.ForeignKey(User , on_delete = models.CASCADE)
    checker = models.IntegerField()
    question = models.ForeignKey(ExamQuestions , on_delete=models.CASCADE)
    indi_student = models.ForeignKey(Indivisuals , on_delete=models.CASCADE , blank=True , null=True)
    teach_student = models.ForeignKey(TeacherClassStudents , on_delete=models.CASCADE , blank=True , null=True)
    obtained = models.IntegerField()
    def __str__(self):
        if str(self.indi_student) == 'None':
            return 'Answer Of {} , Checked By {}'.format(self.teach_student,self.checker)
        else:
            return 'Answer Of {} , Checked By {}'.format(self.indi_student,self.checker)

class Guide(models.Model):
    code = models.AutoField(primary_key=True)
    subject = models.ForeignKey(Subjects ,on_delete=models.CASCADE)
    url = models.URLField(max_length=500)
