from django.urls import path
from . import views

app_name = 'Matching'

urlpatterns = [
    path('',views.ManageRelationshipMatchingListView, name='list'),
    path('match/',views.ManageRelationshipMatchingSaveView, name='match'),
    path('matched/list',views.ManageRelationshipMatchedListView, name='matched_list'),
]