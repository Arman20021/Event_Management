from django.urls import path
from tasks.views import manager_dashboard,employee_dashboard, create_task,view_task,update_task,delete_task,event_manage,task_details,dashboard,participant_details,rsvp_task,my_events
urlpatterns = [
     path('manager-dashboard/',manager_dashboard,name='manager-dashboard'),
     path('user-dashboard/', employee_dashboard, name='user-dashboard'),

 
     path('create-task/',create_task,name='create-task'),
     path('view_task/',view_task),
     path('update_task/<int:id>/',update_task,name='update-task'),
     path('delete_task/<int:id>/',delete_task,name='delete-task'),
     path('event_manage/',event_manage,name='event_manage'),
  
     path('task/<int:task_id>/details/', task_details, name='task-details'),
     path('participant/<int:task_id>/details/', participant_details, name='participant-details'),
     path('dashboard/',dashboard, name='dashboard'),
     path('task/<int:task_id>/rsvp/', rsvp_task, name='rsvp-task'),
     path('my-events/', my_events, name='my-events'),
  




]
