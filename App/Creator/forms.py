from django import forms
from .models import Creator



class ManageCreatorCreateForm(forms.ModelForm):
    class Meta:
        model = Creator
        fields = [
            'name' ,
            'user' ,
            'mobile' ,
            'nic' ,
            'bank_account' ,
            'easypaisa' ,
        ]
