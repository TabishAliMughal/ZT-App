from django.forms import *
from django import forms
from .models import *
from mapwidgets.widgets import GooglePointFieldWidget




class TeacherClassStudentCreateForm(forms.ModelForm):
    class Meta:
        model = TeacherClassStudents
        fields = [
            'id' ,
            'clas' ,
            'name' ,
            'father_name' ,
            'contact' ,
            'address' ,
            'picture' ,
        ]

class TeacherClassCreateForm(forms.ModelForm):
    class Meta:
        model = TeacherClass
        fields = (
            'teacher' ,
            'clas' ,
            'limit' ,
            'school',
            'location',
            'session',
        )
        widgets = {
            'location': GooglePointFieldWidget,
        }
