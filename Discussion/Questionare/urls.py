from django.urls import path
from . import views

app_name = 'Questionare'

urlpatterns = [
    path('', views.ManageQuestionsListView, name='questions'),
    path('questions/ask', views.ManageUserQuestionAskView, name='ask_question'),
    path('questions/user/<user>', views.ManageQuestionsListView, name='my_question'),
    path('questions/answer', views.ManageQuestionAnswerView, name='answer_question'),
]