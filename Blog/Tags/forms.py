from django import forms
from .models import Tags , BlogTags , PostTags



class ManageTagsCreateForm(forms.ModelForm):
    class Meta:
        model = Tags
        fields = [
            'name' ,
        ]

class ManageBlogTagsCreateForm(forms.ModelForm):
    class Meta:
        model = BlogTags
        fields = [
            'blog' ,
            'tag' ,
        ]
        
class ManagePostTagsCreateForm(forms.ModelForm):
    class Meta:
        model = PostTags
        fields = [
            'post' ,
            'tag' ,
        ]