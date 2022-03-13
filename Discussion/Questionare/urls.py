from django.urls import path
from . import views

app_name = 'Questionare'

urlpatterns = [
    path('', views.ManageQuestionsListView, name='questions'),
    path('questions/ask', views.ManageUserQuestionAskView, name='ask_question'),
    path('questions/user/<user>', views.ManageQuestionsListView, name='my_question'),
    path('questions/answer', views.ManageQuestionAnswerView, name='answer_question'),
    path('questions/<question>/audiance', views.ManageQuestionAudianceView, name='question_audiance'),
    path('questions/answer/approve/<answer>', views.ManageApproveAnswer, name='question_answer_approve'),
]