from django.forms import *
from django import forms
from .models import *

class ManageSchoolCreateForm(forms.ModelForm):
    class Meta:
        model = School
        fields = [
            'school' ,
            'address' ,
            'user' ,
        ]