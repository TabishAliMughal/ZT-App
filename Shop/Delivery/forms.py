from django import forms
from .models import *
from mapwidgets.widgets import GooglePointFieldWidget

class ManageDeliveryPersonDataForm(forms.ModelForm):
    class Meta:
        model = DeliveryPerson
        fields = [
            'user',
            'name',
            'start_time',
            'end_time',
            'active',
            'mobile',
            'nic',
            'bank_account',
            'easypaisa',
            'area',
        ]
        widgets = {
            'area': GooglePointFieldWidget,
        }

class ManageDeliveryPersonTasksForm(forms.ModelForm):
    class Meta:
        model = DeliveryTasks
        fields = [
            'person' ,
            'order' ,
            'task_from' ,
            'task_to' ,
            'status' ,
        ]


class ManageDeliveryProofForm(forms.ModelForm):
    class Meta:
        model = DeliveryProof
        fields = [
            'order',
            'image',
        ]
