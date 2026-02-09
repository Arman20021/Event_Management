from django.contrib import admin
from .models import Task,TaskDetail,Project

 
admin.site.register(Task)
admin.site.register(TaskDetail)
# admin.site.register(Employee)
admin.site.register(Project)