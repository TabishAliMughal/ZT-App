from django.urls import path
from . import checkerviews

app_name = 'Checker'

urlpatterns = [
    path('',checkerviews.ManageCheckerProfileView, name='checker_profile'),
    path(r'class/full/\d12345<pk>910\d/\d12345<id>910\d/',checkerviews.ManageCheckerClassView, name='full_class'),
    path(r'class/create/\d12345<pk>910\d',checkerviews.ManageCheckerClassCreateView, name='checker_class_create'),
    path(r'class/check/\d12345<student>910\d/\d12345<checker>910\d/\d12345<clas>910\d',checkerviews.ManageCheckerCheckView, name='student_copy_check'),
    path(r'class/check/claimed\d12345<exam>910\d/\d12345<student>910\d/',checkerviews.ManageCheckerStudentCopyCheckClaimView, name='student_copy_claim'),
]