from django import forms
from .models import Creator , UserData



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



class ManageUserDataForm(forms.ModelForm):
    class Meta:
        model = UserData
        fields = [
            'user' ,
            'picture' ,
            'first_name' ,
            'address' ,
            'city' ,
            'mobile' ,
            'nic' ,
            'bank_account' ,
            'easypaisa' ,
        ]