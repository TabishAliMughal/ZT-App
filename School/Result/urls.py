from django.urls import path
from . import resultviews

app_name = 'Result'


urlpatterns = [
    path(r'teacher/class/student/result/\d12345<id>910\d/\d12345<pk>910\d',resultviews.ManageTeacherClassStudentResultView, name='teacher_class_student_result'),
    path(r'teacher/class/student/result/answers/\d12345<exam>910\d/\d12345<student>910\d',resultviews.ManageTeacherClassStudentResultAnswersView, name='teacher_class_student_result_answers'),
    path(r'teacher/class/student/result/\d12345<id>910\d/',resultviews.ManageTeacherClassResultView, name='teacher_class_result'),
    path(r'teacher/class/student/result/print/\d12345<id>910\d/',resultviews.ManageTeacherClassResultPrintView, name='teacher_class_result_print'),
]