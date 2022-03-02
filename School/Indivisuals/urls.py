from django.urls import path
from . import views
from . import indivisualviews

app_name = 'Indivisuals'


urlpatterns = [
    path(r'',views.ManageIndivisualsListView, name='indivisuals_list'),
    path(r'school/<pk>/all/',views.ManageIndivisualsListView, name='indivisuals_list'),
    path(r'detail/<pk>',views.ManageIndivisualsDetailView, name='indivisuals_detail'),
    path(r'create',views.ManageIndivisualsCreateView, name='indivisuals_create'),
    path(r'edit/<pk>',views.ManageIndivisualsEditView, name='indivisuals_edit'),
    path(r'delete/<pk>',views.ManageIndivisualsDeleteView, name='indivisuals_delete'),

    # for school
    path(r'create/<pk>',views.ManageIndivisualsCreateView, name='indivisuals_create'),


    path(r'individual',indivisualviews.ManageIndivisualProfileView, name='indivisual_profile'),
    path(r'individual/content/<pk>',indivisualviews.ManageIndivisualProfileView, name='indivisual_content'),
    path(r'individual/content/<pk>/documents',indivisualviews.ManageIndivisualDocumentsView, name='content-image'),

    # revision
    path(r'revision/<individual>/<clas>/<subject>',indivisualviews.ManageIndivisualRevisionSubjectView, name='revision_subject'),
]