from django.urls import path
from . import views

app_name = 'Delivery'

urlpatterns = [
    path('list/', views.ManageDeliveryPersonListView, name='delivery_person_list'),
    path('my/data', views.ManageDeliveryPersonDataView, name='delivery_person_data'),



    path('my/tasks', views.ManageDeliveryPersonTasksListView, name='delivery_person_tasks'),
    path('my/task/<task>', views.ManageDeliveryPersonTaskDetailView, name='delivery_person_task_detail'),
    path('my/task/deliver/<task>', views.ManageDeliveryPersonTaskCompleteView, name='delivery_person_task_complete'),
    # path('my/task/deliver/abc', views.ManageDeliveryPersonTaskCompletedView, name='delivery_person_task_complete'),
    path('delivery/task/create', views.ManageDeliveryPersonTasksCreateView, name='delivery_person_tasks_create'),
]