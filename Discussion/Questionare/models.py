from django.db import models
from django.core.exceptions import ValidationError


def validate_file_size(value):
    filesize= value.size
    if filesize > 5242880:
        raise ValidationError("The maximum file size that can be uploaded is 5MB")
    else:
        return value



class Category(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Categories'

class Question(models.Model):
    user = models.IntegerField()
    question = models.CharField(max_length=75)
    text = models.CharField(max_length=500,blank=True,null=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    image = models.FileField(blank=True,null=True,upload_to="Questions/",validators=[validate_file_size])
    video = models.FileField(blank=True,null=True,upload_to="Questions/",validators=[validate_file_size])
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.question
    class Meta:
        verbose_name_plural = 'Questions'

class QuestionAudiance(models.Model):
    user = models.IntegerField()
    question = models.ForeignKey(Question , on_delete=models.CASCADE)
    def __str__(self):
        return self.question
    class Meta:
        verbose_name_plural = 'Question Audiance'

class Answer(models.Model):
    user = models.IntegerField()
    question = models.ForeignKey(Question , on_delete=models.CASCADE)
    answer = models.CharField(max_length=500)
    image = models.FileField(blank=True,null=True,upload_to="Questions/",validators=[validate_file_size])
    video = models.FileField(blank=True,null=True,upload_to="Questions/",validators=[validate_file_size])
    accepted = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.answer
    class Meta:
        verbose_name_plural = 'Answers'

