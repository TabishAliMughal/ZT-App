from django import forms
from django.forms import fields
from .models import Candidates


class ManageCandidateCreateForm(forms.ModelForm):
    class Meta:
        model = Candidates
        fields = [
            'user',
            'name',
            'father_name',
            'image',
            'date_of_birth',
            'age',
            'gender',
            'occupation',
            'education',
            'living_status',
            'cast',
            'siblings',
            'height',
            'mobile',
            'address',
            'cnic',
            'place_of_birth',
            'marital_status',
            'parents',
            'discription',
            'father_occupation',
            'facebook_id',
            'email_address',
            'religion',
            'mother_toungue',
            'monthly_income',
            'matched',
        ]