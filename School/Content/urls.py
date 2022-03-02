from django.urls import path
from . import views
from . import selectviews
from . import formviews
from . import listviews
from . import editviews
from . import deleteviews

app_name = 'Content'

urlpatterns = [
    # Main
    path('',views.ManageMainView, name ='main'),
    path('view/',views.ManageAllView, name ='all'),
    path('demo',views.ManageDemoView, name ='demo'),
    path('demo/<demodate>',views.ManageDemoListView, name ='demo_list'),
    path('demo/<filday>/filter',views.ManageDemoListView, name ='content_by_date'),
    path('demo/<day>/<clas>',views.ManageDemoContentView, name ='demo_content'),
    path('select/add',views.ManageSelectToAddView, name ='select_to_add'),

    # Create
    path('exam/create/',formviews.ManageExamCreateView, name ='exam_form'),
    path('class/create/',formviews.ManageClassesCreateView, name ='class_form'),
    path('module/create/',formviews.ManageModuleCreateView, name ='module_form'),
    path('content/create/',formviews.ManageContentCreateView, name ='content_form'),
    path('subject/create/',formviews.ManageSubjectsCreateView, name ='subject_form'),
    path('classsubject/create/',formviews.ManageClassSubjectsCreateView, name ='class_subject_form'),
    
    # List
    path('class/list/',listviews.ManageClassListView, name ='class'),
    path('exam/list/',listviews.ManageExamListView, name ='exam'),
    path('content/list/',listviews.ManageContentListView, name ='content'),
    path('subject/list/',listviews.ManageSubjectListView, name ='subject'),
    path('module/list/',listviews.ManageModuleListView, name ='module'),
    path('classsubject/list/',listviews.ManageClassSubjectsListView, name ='class_subject'),

    # Edit
    path(r'class/edit/\d12345<pk>910\d/',editviews.ManageClassEditView, name ='class_edit'),
    path(r'exam/edit/\d12345<pk>910\d/',editviews.ManageExamEditView, name ='exam_edit'),
    path(r'content/edit/\d12345<pk>910\d/',editviews.ManageContentEditView, name ='content_edit'),
    path(r'subject/edit/\d12345<pk>910\d/',editviews.ManageSubjectEditView, name ='subject_edit'),
    path(r'module/edit/\d12345<pk>910\d/',editviews.ManageModuleEditView, name ='module_edit'),
    path(r'classsubject/edit/\d12345<pk>910\d/',editviews.ManageClassSubjectsEditView, name ='class_subject_edit'),

    # Delete
    path(r'class/delete/\d12345<pk>910\d/',deleteviews.ManageClassDeleteView, name ='class_delete'),
    path(r'content/delete/\d12345<pk>910\d/',deleteviews.ManageContentDeleteView, name ='content_delete'),
    path(r'content/picture/delete/\d12345<pk>910\d/',deleteviews.ManageContentPictureDeleteView, name ='content_picture_delete'),
    path(r'subject/delete/\d12345<pk>910\d/',deleteviews.ManageSubjectDeleteView, name ='subject_delete'),
    path(r'module/delete/\d12345<pk>910\d/',deleteviews.ManageModuleDeleteView, name ='module_delete'),
    path(r'classsubject/delete/\d12345<pk>910\d/',deleteviews.ManageClassSubjectsDeleteView, name ='class_subject_delete'),

    # Select
    path('teach/date/',selectviews.ManageDateSelectView, name ='date_select'),
    path(r'teach/\d12345<date>910\d/',selectviews.ManageClassSelectView, name ='class_select'),
    path(r'teach/content/\d12345<code>910\d/',selectviews.ManageContentView, name ='content'),
    path(r'teach/\d12345<date>910\d/\d12345<Ccode>910\d/',selectviews.ManageSubjectSelectView, name ='subject_select'),
    path(r'teach/\d12345<date>910\d/\d12345<Ccode>910\d/\d12345<subject>910\d/',selectviews.ManageSessionSelectView, name ='session_select'),
    path(r'teach/\d12345<date>910\d/\d12345<Ccode>910\d/\d12345<subject>910\d/\d12345<session>910\d/',selectviews.ManageContentSelectView, name ='content_select'),

    # Close
    path(r'exam/close/\d12345<pk>910\d/',deleteviews.ManageExamCloseView, name ='exam_close'),

]
