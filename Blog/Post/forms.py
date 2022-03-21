from django import forms
from .models import Post, PostComment, PostReact


class ManagePostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'name',
            'description',
            'text',
            'image',
            'video',
            'sound',
            'blog',
            'views',
        ]

class ManagePostReactForm(forms.ModelForm):
    class Meta:
        model = PostReact
        fields = [
            'user',
            'post',
            'react',
        ]

class ManagePostCommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = [
            'user',
            'post',
            'comment',
        ]