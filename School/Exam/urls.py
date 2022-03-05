from django.urls import path
from . import views
from . import examquestionviews

app_name = 'Exam'

urlpatterns = [
    path(r'exam/questions/\d12345<id>910\d/',examquestionviews.ManageExamQuestionsView, name='exam_questions'),
    path(r'exam/questions/edit/\d12345<id>910\d/',examquestionviews.ManageExamEditQuestionsView, name='exam_questions_edit'),
    path(r'exam/questions/delete/\d12345<id>910\d/',examquestionviews.ManageContentDeleteView, name='exam_questions_delete'),
    path(r'exam/question/create/\d12345<id>910\d/',examquestionviews.ManageExamAddQuestionsView, name='exam_questions_add'),

    path(r'class/students/exam/\d12345<id>910\d/',views.ManageClassExamView, name='teacher_class_exam'),
    path(r'class/students/exam/print/questions/\d12345<id>910\d/',views.ManageClassExamQuestionPrintView, name='exam_print_questions'),
    path(r'class/students/exam/print/file/\d12345<id>910\d/',views.ManageClassExamFilePrintView, name='exam_print_file'),
    path(r'class/student/exam/upload/picture/\d12345<id>910\d/',views.ManageAddStudentExamPictureView, name='exam_upload_pictures_1'),
    path(r'class/student/exam/upload/picture/\d12345<id>910\d/\d12345<pk>910\d/',views.ManageAddStudentExamPictureView, name='exam_upload_pictures'),
    path(r'class/exam/answers/select/\d12345<id>910\d/\d12345<pk>910\d/',views.ManageTeacherClassExamAnswersStudentSelectView, name ='teacher_class_exam_answers_student_select'),

]