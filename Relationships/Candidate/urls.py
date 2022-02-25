from django.urls import path
from . import views

app_name = 'Matching'

urlpatterns = [
    path('candidate/',views.ManageRelationshipCandidateInfoView, name='info'),
    path('candidate/add',views.ManageRelationshipCandidateInfoAddView, name='add_data'),
    path('candidate/edit',views.ManageRelationshipCandidateInfoAddView, name='edit_data'),
    path('candidate/matches/list',views.ManageRelationshipCandidateMatchesListView, name='candidate_matches'),
    path('candidate/candidate/list',views.ManageRelationshipCandidateListView, name='candidate_list'),
]