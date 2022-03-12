from django import forms
from .models import Answer, Question, QuestionAudiance


class AskQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            'user',
            'question',
            'text',
            'category',
            'image',
            'video',
        ]

class AnswerQuestionForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = [
            'user',
            'question',
            'answer',
            'image',
            'video',
            'accepted',
        ]

class QuestionAudianceForm(forms.ModelForm):
    class Meta:
        model = QuestionAudiance
        fields = [
            'user',
            'question',
        ]