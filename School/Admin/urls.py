from django.urls import path
from . import adminviews

app_name = 'Admin'

urlpatterns = [
    path('profiles',adminviews.ManageProfilesView, name='profiles'),
    path('activation/',adminviews.ManageActiveAndDeactiveView, name='active_deactive'),
    path('activation/by/school',adminviews.ManageActiveAndDeactiveBySchoolView, name='active_deactive_by_school'),
    path('activation/by/school/activete',adminviews.ManageActivateSchoolView, name='activate_school'),
    path('activation/by/school/deactivate',adminviews.ManageDeactivateSchoolView, name='deactivate_school'),
]