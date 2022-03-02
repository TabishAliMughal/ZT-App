from School.Exam.models import ExamStatus
from django import *
from django import forms
from django.forms import ModelForm
from .models import *
from School.Requirments.models import *


class ClassesForm(forms.ModelForm):
    class Meta:
        model = Classes
        fields = [
            'serial',
            'class_name',
        ]

class SubjectsForm(forms.ModelForm):
    class Meta:
        model = Subjects
        fields = [
            'subject_name',
        ]

class ClassSubjectsForm(forms.ModelForm):
    class Meta:
        model = ClassSubjects
        fields = [
            'class_name',
            'subject_name',
        ]

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = [
            'module',
        ]

class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = [
            'class_name',
            'subject',
            'module',
            'day',
            'title',
            'text',
            'therefor',
        ]

class VideoForm(forms.ModelForm):
    class Meta:
        model = Videos
        fields = [
            'content' ,
            'url' ,
        ]
        
class ImageForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = [
            'content' ,
            'image' ,
        ]

class VisitsForm(forms.ModelForm):
    class Meta:
        model = Visits
        fields = [
            'page' ,
            'visits' ,
            'date' ,
        ]

class ExamForm(forms.ModelForm):
    class Meta:
        model = ExamStatus
        fields = [
            'exam_number' ,
            'class_name' ,
            'subject' ,
            'session' ,
            'status' ,
        ]