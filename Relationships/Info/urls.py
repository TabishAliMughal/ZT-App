from django.urls import path
from . import views

app_name = 'Info'

urlpatterns = [
    path('',views.ManageRelationshipHomeView, name='home'),
]