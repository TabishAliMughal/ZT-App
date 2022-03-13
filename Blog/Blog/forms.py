from django import forms
from .models import Blog


class ManageBlogCreateForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = [
            'name' ,
            'description',
            'image' ,
            'type' ,
            'user' ,
            'views' ,
        ]
