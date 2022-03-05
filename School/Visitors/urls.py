from django.urls import path
from . import listviews
from . import formviews

app_name = 'Visitors'


urlpatterns = [
    path(r'Teacher/Visit',listviews.ManageTeacherVisitListView, name='visited_Teachers_list'),
    path(r'School/Visit',listviews.ManageSchoolVisitListView, name='visited_Schools_list'),
    path(r'Parent/Visit',listviews.ManageParentVisitListView, name='visited_Parents_list'),

    path(r'Teacher/Visit/Create',formviews.ManageTeacherVisitCreateView, name='visited_Teachers_create'),
    path(r'School/Visit/Create',formviews.ManageSchoolVisitCreateView, name='visited_Schools_create'),
    path(r'Parent/Visit/Create',formviews.ManageParentVisitCreateView, name='visited_Parents_create'),

]