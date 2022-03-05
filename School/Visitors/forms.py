from django.forms import *
from django import forms
from .models import *




class ManageTeacherVisitForm(forms.ModelForm):
    class Meta:
        model = TeacherVisit
        fields = [
            'name' ,
            'phone' ,
            'email' ,
            'seen' ,
        ]


class ManageSchoolVisitForm(forms.ModelForm):
    class Meta:
        model = SchoolVisit
        fields = [
            'name' ,
            'school_name' ,
            'phone' ,
            'email' ,
            'seen' ,
        ]


class ManageParentVisitForm(forms.ModelForm):
    class Meta:
        model = ParentVisit
        fields = [
            'name' ,
            'student_name' ,
            'phone' ,
            'email' ,
            'seen' ,
        ]