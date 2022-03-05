from django.forms import *
from django import forms
from .models import *

class ManageCheckerClassCreateForm(forms.ModelForm):
    class Meta:
        model = CheckerClass
        fields = [
            'checker' ,
            'subject' ,
        ]