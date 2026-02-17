from django.shortcuts import render,redirect
from django.http import HttpResponse
from tasks.forms import TaskForm,TaskModelForm,TaskDetailModelForm    
from tasks.models import *
from datetime import date
from django.db.models import Q,Count,Min,Max,Avg
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test,login_required,permission_required
from users.views import is_admin
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.base import ContextMixin
from django.views.generic import ListView,DetailView
# Create your views here.


 

# views.py
def is_manager(user):
 
    return user.groups.filter(name__iexact='Manager').exists()

def is_participant(user):
    return user.groups.filter(name__iexact='Participant').exists()



@login_required
@user_passes_test(is_manager,login_url='no-permission')
def manager_dashboard(request):
    type_filter = request.GET.get('type', 'all')
    query = request.GET.get('q', '').strip()  # search text

    # Status counts
    counts = Task.objects.aggregate(
        total=Count('id'),
        completed=Count('id', filter=Q(status="COMPLETED")),
        in_progress=Count('id', filter=Q(status="IN_PROGRESS")),
        pending=Count('id', filter=Q(status="PENDING"))
    )

    # Base query
    tasks = Task.objects.select_related('details').prefetch_related('assigned_to')

    # Apply status filter
    if type_filter == 'completed':
        tasks = tasks.filter(status='COMPLETED')
    elif type_filter == 'in-progress':
        tasks = tasks.filter(status='IN_PROGRESS')
    elif type_filter == 'pending':
        tasks = tasks.filter(status='PENDING')

    # Apply search filter only on title
    if query:
        tasks = tasks.filter(title__icontains=query)

    context = {
        'tasks': tasks,
        'counts': counts,
        'query': query,
        'type': type_filter,
        'role':'manager'
    }

    return render(request, "dashboard/manager-dashboard.html", context)



@login_required
@user_passes_test(is_participant,login_url='no-permission')
def employee_dashboard(request):
    type_filter = request.GET.get('type', 'all')
    query = request.GET.get('q', '').strip()  # search text

    # Status counts
    counts = Task.objects.aggregate(
        total=Count('id'),
        completed=Count('id', filter=Q(status="COMPLETED")),
        in_progress=Count('id', filter=Q(status="IN_PROGRESS")),
        pending=Count('id', filter=Q(status="PENDING"))
    )

    # Base query
    tasks = Task.objects.select_related('details').prefetch_related('assigned_to')

    # Apply status filter
    if type_filter == 'completed':
        tasks = tasks.filter(status='COMPLETED')
    elif type_filter == 'in-progress':
        tasks = tasks.filter(status='IN_PROGRESS')
    elif type_filter == 'pending':
        tasks = tasks.filter(status='PENDING')

    # Apply search filter only on title
    if query:
        tasks = tasks.filter(title__icontains=query)

    context = {
        'tasks': tasks,
        'counts': counts,
        'query': query,
        'type': type_filter,
        'role':'manager'
    }

    return render(request, "dashboard/user_dashboard.html", context)




    
@login_required   
@permission_required("tasks.add_task",login_url='no-permission' )
def create_task(request): 
    task_form = TaskModelForm()
    task_detail_form = TaskDetailModelForm()

    if request.method == "POST":
        # Add request.FILES here!
        task_form = TaskModelForm(request.POST, request.FILES)
        task_detail_form = TaskDetailModelForm(request.POST)
        
        if task_form.is_valid() and task_detail_form.is_valid():
            task = task_form.save()
            task_detail=task_detail_form.save(commit=False)
            task_detail.task=task
            task_detail.save()
            messages.success(request,"Task Created Successfully")

            return redirect ('manager-dashboard')

    context={"task_form":task_form,'task_detail_form':task_detail_form}
    return render (request,"dashboard/task_form.html",context)



#create decorators for class based view

create_decorators=[permission_required("tasks.add_task",login_url='no-permission' ),login_required]

class CreateTask(ContextMixin,LoginRequiredMixin,PermissionRequiredMixin,View):
    permission_required="tasks.add_task"
    login_url='no-permission'
    
    def get_context_data(self, **kwargs)  :
        context = super().get_context_data(**kwargs)
        context['task_form']=kwargs.get('task_form',TaskModelForm) 
        context['task_detail_form']=kwargs.get('task_detail_form',TaskDetailModelForm) 
        return context
    


    def get(self,request,*args,**kwargs):
 
        context=self.get_context_data()
        return render (request,"dashboard/task_form.html",context)
    

    def post(self,request,*args,**kwargs):
        task_form = TaskModelForm(request.POST, request.FILES)
        task_detail_form = TaskDetailModelForm(request.POST)
        
        if task_form.is_valid() and task_detail_form.is_valid():
            task = task_form.save()
            task_detail=task_detail_form.save(commit=False)
            task_detail.task=task
            task_detail.save()
            messages.success(request,"Task Created Successfully")
            context=self.get_context_data(task_form=task_form,task_detail_form=task_detail_form)
            return redirect ('manager-dashboard')




@login_required 
@permission_required("tasks.view_task",login_url='no-permission' )
def view_task(request):
   
    task_count=Task.objects.aggregate(num_task=Count('id'))
  

    return render (request,"show_task.html",{"task_count":task_count})




class ViewTask(ListView):
    model=Project
    context_object_name='projects'
    template_name='show_task.html'








@login_required   
@permission_required("tasks.change_task",login_url='no-permission')
def update_task(request, id): 
    task = Task.objects.get(id=id)
    
    # Check if task has details to avoid RelatedObjectDoesNotExist errors
    task_details = getattr(task, 'details', None)

    if request.method == "POST":
        # Data is being submitted
        task_form = TaskModelForm(request.POST, request.FILES, instance=task)
        task_detail_form = TaskDetailModelForm(request.POST, instance=task_details)
        
        if task_form.is_valid() and task_detail_form.is_valid():
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()
            messages.success(request, "Task Updated Successfully")
            return redirect('update-task', id=id)
    else:
        # This is a GET request - Show the forms with existing data
        task_form = TaskModelForm(instance=task)
        task_detail_form = TaskDetailModelForm(instance=task_details)

    # Now these variables exist whether it was a POST or a GET request
    context = {
        "task_form": task_form,
        'task_detail_form': task_detail_form
    }
    return render(request, "dashboard/task_form.html", context)



@login_required   
@permission_required("tasks.delete_task",login_url='no-permission')
def delete_task(request,id):
    if request.method == 'POST':
        task=Task.objects.get(id=id)
        task.delete()
        messages.success(request,"Task is Deleted")
        return redirect('manager-dashboard')
    else:
       messages.error(request,"Something went wrong")
       return redirect ('manager-dashboard')


def event_manage(request):
    return render (request,"dashboard/event_manage.html" )

 

 




@login_required   
@permission_required("tasks.delete_task",login_url='no-permission')
def task_details(request,task_id):
  
    
    task=Task.objects.get(id=task_id) 
    status_choices=Task.STATUS_CHOICES

    if request.method=='POST':
        selected_status=request.POST.get('task_status')
        task.status=selected_status
        task.save()
        return redirect('task-details',task.id)
    return render (request,'task_details.html',{'task':task,'status_choices':status_choices})







 












@login_required   
@permission_required("tasks.delete_task",login_url='no-permission')
def participant_details(request,task_id):
  
    
    task=Task.objects.get(id=task_id) 
    event = getattr(task, 'event', None) 
    status_choices=Task.STATUS_CHOICES

    if request.method=='POST':
        selected_status=request.POST.get('task_status')
        task.status=selected_status
        task.save()
        return redirect('participant-details',task.id)
    return render (request,'participant_details.html',{'task':task,'status_choices':status_choices, 'event': event})


@login_required
def dashboard(request):
    if is_manager(request.user):
        return redirect('manager-dashboard')
    elif is_participant(request.user):
        return redirect('user-dashboard')
    elif is_admin(request.user):
        return redirect('admin-dashboard')

    # return redirect('no-permission')

# tasks/views.py

@login_required
def rsvp_task(request, task_id):
    task = Task.objects.get(id=task_id)
    if task.attendees.filter(id=request.user.id).exists():
        messages.warning(request, f"You have already joined the task: {task.title}")
    else:
        task.attendees.add(request.user)
        
       
        send_mail(
            'RSVP Confirmation',
            f'You have successfully RSVP\'d for the task/event: {task.title}',
            'mdarmanislam20021@gmail.com',
            [request.user.email],
            fail_silently=True,
        )
        messages.success(request, f"Successfully joined {task.title}!")

    return redirect('my-events')

@login_required
def my_events(request):
    # This now matches the related_name='rsvp_tasks' in Task model
    tasks = request.user.rsvp_tasks.all() 
    return render(request, 'my_events.html', {'tasks': tasks})