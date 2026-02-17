from django.db import models
 
from django.conf import settings
 
 

class Project(models.Model):
    name=models.CharField(max_length=100)
    start_date=models.DateField()
    description=models.TextField(blank=True,null=True)

    def __str__(self):
        return self.name

# Create your models here.
class Task(models.Model):

    attendees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='rsvp_tasks', blank=True)

    STATUS_CHOICES=[
        ('PENDING','Pending'),
        ('IN_PROGRESS','In Progress'),
        ('COMPLETED','Compelted')
    
    ]
    project=models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        default=1
    )
    # assigned_to=models.ManyToManyField(Employee,related_name='tasks')
    assets=models.ImageField(upload_to='task_asset',blank=True,null=True)
    assigned_to=models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='tasks')
    title=models.CharField(max_length=250)
    description=models.TextField()
    due_date=models.DateField()
    status=models.CharField(max_length=15,choices=STATUS_CHOICES,default='PENDING')
    image = models.ImageField(
        upload_to='task_images/',
        blank=True,
        null=True
    )
    # is_completed=models.BooleanField(default=False)
    create_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.title

class TaskDetail(models.Model):
    HIGH='H'
    MEDIUM='M'
    LOW='L'
    PRIORITY_OPTIONS=(
        (HIGH,'High'),
        (MEDIUM,'Medium'),
        (LOW,'Low')
    )
    task=models.OneToOneField(Task,on_delete=models.DO_NOTHING,related_name='details')
    #assigned_to=models.CharField(max_length=100)
    priority=models.CharField(max_length=1,choices=PRIORITY_OPTIONS,default=LOW)
    notes=models.TextField(blank=True,null=True)

    def __str__(self):
        return f"Details for Task {self.task.title}"








class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    attendees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='rsvp_events', blank=True)

   

    def __str__(self):
        return self.name

class Participant(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    events = models.ManyToManyField(Event)

    def __str__(self):
        return self.name



