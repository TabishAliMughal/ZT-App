from django import forms
from .models import *



class ManageDeliveryPersonDataForm(forms.ModelForm):
    class Meta:
        model = DeliveryPerson
        fields = [
            'user',
            'name',
            'start_time',
            'end_time',
            'active',
        ]

class ManageDeliveryPersonTasksForm(forms.ModelForm):
    class Meta:
        model = DeliveryTasks
        fields = [
            'person' ,
            'order' ,
            'task_from' ,
            'task_to' ,
            'status' ,
            'date' ,
        ]


class ManageDeliveryProofForm(forms.ModelForm):
    class Meta:
        model = DeliveryProof
        fields = [
            'order',
            'image',
        ]
