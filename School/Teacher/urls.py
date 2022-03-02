from django.urls import path
from . import teacherviews

app_name = 'Teacher'

urlpatterns = [
    # View
    path('',teacherviews.ManageTeacherProfileView, name='teacher_profile'),
    path(r'class/students/\d12345<id>910\d/',teacherviews.ManageTeacherClassView, name='teacher_class'),
    path(r'class/create/\d12345<id>910\d/',teacherviews.TeacherClassCreateView, name='teacher_class_create'),
    # Student
    path(r'class/student/add/\d12345<id>910\d/',teacherviews.ManageAddStudentView, name ='add_student'),
    path(r'class/student/edit/\d12345<id>910\d/\d12345<pk>910\d',teacherviews.ManageEditStudentView, name ='edit_student'),
    path(r'class/student/delete/\d12345<id>910\d/\d12345<pk>910\d',teacherviews.ManageDeleteStudentView, name ='delete_student'),
]