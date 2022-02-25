from django import forms
from django.forms import fields
from .models import Bunch , BunchPost


class ManageBunchCreateForm(forms.ModelForm):
    class Meta:
        model = Bunch
        fields = [
            'name' ,
            'blog' ,
        ]

class ManageBunchPostCreateForm(forms.ModelForm):
    class Meta:
        model = BunchPost
        fields = [
            'bunch' ,
            'post' ,
        ]