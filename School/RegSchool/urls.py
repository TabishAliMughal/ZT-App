from django.urls import path
from . import schoolviews

app_name = 'RegSchool'


urlpatterns = [
    path('',schoolviews.ManageSchoolProfileView, name='school_profile'),
    path('create/',schoolviews.ManageSchoolCreateView, name='school_create'),
    path(r'teacher/detail/\d12345<id>910\d',schoolviews.ManageTeacherProfileDetailView, name='teacher_profile_detail'),
]