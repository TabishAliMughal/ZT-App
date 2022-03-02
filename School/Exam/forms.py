from django.forms import *
from django import forms
from .models import *


class ManageExamQuestionsForm(forms.ModelForm):
    class Meta:
        model = ExamQuestions
        fields = [
            'exam' ,
            'question' ,
            'marks' ,
        ]


class ManageExamAnswersForm(forms.ModelForm):
    class Meta:
        model = ExamAnswers
        fields = [
            'indi_student',
            'teach_student',
            'exam' ,
            'picture' ,
            'checker' ,
            'checked' ,
        ]


class ManageCheckingSaveForm(forms.ModelForm):
    class Meta:
        model = QuestionsChecked
        fields = [
            'checker' ,
            'question' ,
            'indi_student' ,
            'teach_student' ,
            'obtained' ,
        ]