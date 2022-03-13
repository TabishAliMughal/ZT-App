from django.urls import path
from . import views

app_name = 'User'

urlpatterns = [
    # path('creator/register', views.ManageCreatorCreateView,name='creator_create'),
    # User
    path('profile/', views.ManageUserProfileView, name='user_profle'),
    path('profile/edit', views.ManageUserProfileEditView, name='user_profle_edit'),
    path('profile/edit/access', views.ManageUserAccessView, name='manage_access'),
    path('profile/edit/access/shop', views.ManageUserChangeAccessToShopView, name='change_access_to_shop'),
    path('profile/edit/access/blog', views.ManageUserChangeAccessToBlogView, name='change_access_to_blog'),
]