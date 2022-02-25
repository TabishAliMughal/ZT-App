from django import forms
from .models import Match


class ManageCandidateMatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = [
            'user',
            'male',
            'female',
            'male_side_agree',
            'female_side_agree',
            'active',
            'processed',
        ]